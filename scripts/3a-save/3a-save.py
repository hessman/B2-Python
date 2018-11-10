#!/usr/bin/env python3

# 3a-save.py
# Backup tool
# Anthony DOMINGUE
# 01/11/2018

import tarfile
import hashlib
import signal
import json
import sys
import os

backup_dir = "./data"
config_dir = "./.config"
hashes_json = config_dir + "/hashes.json"

dir_to_backup = "./things"
output_filename = os.path.basename(dir_to_backup)


def terminate(code: int, message=""):
    """
    Properly exit the script with the good verbose.
    :param code: The exit code or sig.
    :type code: int
    :param message: Optional, the message will be print if str.
    """
    if code == 0:
        sys.stdout.write(message)
        sys.stdout.write("\nExiting...\n")
        sys.exit(0)
    else:
        if isinstance(message, str):
            sys.stderr.write("Error " + str(code) + " :\n" + message)
        sys.stderr.write("\nExiting...\n")
        sys.exit(code)


signal.signal(signal.SIGTERM, terminate)
signal.signal(signal.SIGINT, terminate)


def to_tar_gz(source: str, output: str):
    """
    Compress the source in tar.gz into the output.
    :param source: Path of the directory to compress.
    :type source: str
    :param output: Path of the output of the archive.
    :type output: str
    """
    with tarfile.open(output, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))


def get_directory_hash(directory: str):
    """
    Give a SHA256 hash of the whole given directory by hashing recursively and hash the array of hashes.
    It hash files content, files name and directories name.
    :param directory: Path of the directory to hash.
    :type directory: str
    :return: hex sha256 hash of the directory.
    """
    sys.stdout.write("Computing hash...\n")
    hashes = []
    for dir_path, dir_names, file_names in os.walk(directory):
        sha256 = hashlib.sha256()
        for file_name in file_names:
            sha256.update(str(dir_names).encode("utf-8"))
            sha256.update(str(file_name).encode("utf-8"))
            with open(dir_path + '/' + file_name, 'rb') as f:
                # Process file 4096bytes per 4096bytes so the RAM will not be full
                for block in iter(lambda: f.read(4096), b''):
                    sha256.update(block)
            hashes.append(sha256.hexdigest())
    sha256 = hashlib.sha256()
    for h in hashes:
        sha256.update(h.encode("utf-8"))
    sys.stdout.write("Done !\n")
    return sha256.hexdigest()


def initialisation():
    """
    Check if required directories and files exist and create them if needed.
    """
    sys.stdout.write("Initialisation...\n")
    if not os.path.isdir(dir_to_backup):
        terminate(100, "No directory to backup !")
    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
        except Exception as error:
            terminate(error.args[0], str(error))
    if not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir)
        except Exception as error:
            terminate(error.args[0], str(error))
    if not os.path.exists(hashes_json):
        try:
            with open(hashes_json, 'a+') as f:
                f.write("{}")
        except Exception as error:
            terminate(error.args[0], str(error))
    # Check if the hashes_json file is a valid json, if not repair it
    if os.path.exists(hashes_json):
        try:
            with open(hashes_json, 'r') as f:
                json.load(f)
        except Exception as error:
            sys.stderr.write("Error " + str(error.args[0]) +
                             "\nInvalid " + hashes_json + " file...\nTry repairing it...\n")
            try:
                with open(hashes_json, 'w') as f:
                    f.write("{}")
            except Exception as error:
                terminate(error.args[0], str(error))
    sys.stdout.write("Done !\n")


def local_backup(directory: str, new_hash: str):
    """
    Backup locally to the backup_dir.
    :param directory: Path of the directory to backup.
    :type directory: str
    :param new_hash: The hash of the directory to backup.
    :type new_hash: str
    """
    sys.stdout.write("Local backup in progress...\n")
    try:
        to_tar_gz(directory, backup_dir + '/' + output_filename)
        sys.stdout.write("Done !\n")
        update_json(directory, new_hash)
    except Exception as error:
        terminate(error.args[0], str(error))


def update_json(directory: str, new_hash: str):
    """
    Update the hashes_json with directory as key and new_hash as value.
    :param directory: Path of the backed up directory.
    :type directory: str
    :param new_hash: The hash of the new backed up directory.
    :type new_hash: str
    """
    sys.stdout.write("Updating entries...\n")
    try:
        with open(hashes_json, 'r+') as f:
            data = json.load(f)
            data[directory] = new_hash
            # Rewrite the new hashes_json
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        terminate(0, "Done !")
    except Exception as error:
        terminate(error.args[0], str(error))


def check_for_changes(directory: str):
    """
    Compare hash in hashes_json and the return of get_directory_hash for a given directory.
    :param directory: The directory to check and eventually backup.
    :type directory: str
    :return result: Dictionary that contains hash of the directory to check and bool about the checking.
    """

    # I use a dictionary as return for more readability
    result = {"hash": get_directory_hash(directory)}

    with open(hashes_json, 'r') as f:
        data = json.load(f)

    sys.stdout.write("computed hash for " + directory + " : " + result["hash"] + "\n")

    if directory in data:
        sys.stdout.write("founded  hash for " + directory + " : " + data[directory] + " in " + hashes_json + "\n")
        if result["hash"] == data[directory]:
            sys.stdout.write("Same hashes !\n")
            result["isPositive"] = False
            return result
        else:
            sys.stdout.write("Different hashes !\n")
            result["isPositive"] = True
            return result
    else:
        sys.stdout.write("no hash found for " + directory + " in " + hashes_json + "\n")
        sys.stdout.write("New archive !\n")
        result["isPositive"] = True
        return result


initialisation()

check_result = check_for_changes(dir_to_backup)
if check_result["isPositive"]:
    local_backup(dir_to_backup, check_result["hash"])
else:
    terminate(0, "Work is done !")
