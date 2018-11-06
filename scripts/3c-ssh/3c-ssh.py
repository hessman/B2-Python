#!/usr/bin/python3

# 3c-ssh.py
# Backup tool
# Anthony DOMINGUE
# 06/11/2018

import paramiko
import argparse
import tarfile
import hashlib
import signal
import json
import sys
import os

config_dir = "./.config"
hashes_json = config_dir + "/hashes.json"


def terminate(code: int, message=""):
    """
    Properly exit the script with the good verbose.
    :param code: The exit code or sig.
    :type code: int
    :param message: Optional, the message will be print if str.
    """
    if code == 0:
        write_stdout(message)
        write_stdout("\nExiting...\n")
        sys.exit(0)
    else:
        if isinstance(message, str):
            sys.stderr.write("Error " + str(code) + " :\n" + message)
        sys.stderr.write("\nExiting...\n")
        sys.exit(code)


def write_stdout(message: str):
    """
    Write message in sys.stdout if not in quiet mode.
    :param message: Message to sys.stdout.write
    :type message: str
    """
    if not quiet:
        sys.stdout.write(message)


signal.signal(signal.SIGTERM, terminate)
signal.signal(signal.SIGINT, terminate)

parser = argparse.ArgumentParser(description="A simple backup tool",
                                 epilog="Example :./3c-ssh.py -s ./things ./other_things -o ./data",
                                 prog="3b-opt")

basic_args = parser.add_argument_group('required arguments')
ssh_args = parser.add_argument_group('optional ssh arguments')

parser.add_argument("-q", "--quiet",
                    help="quiet mode, no stdout",
                    action="store_true")

# Basic arguments group
basic_args.add_argument("-s", "--sources",
                        nargs="+",
                        help="path to the directories to backup",
                        required=True,
                        type=str)
basic_args.add_argument("-o", "--output",
                        help="path where the directories will be backed up",
                        required=True,
                        type=str)
# SSH arguments group
ssh_args.add_argument("-p", "--port",
                      help="ssh port for distant server",
                      type=str)
ssh_args.add_argument("-a", "--address",
                      help="address for distant server",
                      type=str)
ssh_args.add_argument("-u", "--username",
                      help="ssh username for distant server",
                      type=str)
ssh_args.add_argument("-P", "--password",
                      help="ssh password for distant server",
                      type=str)

args = parser.parse_args()

quiet = args.quiet
dirs_to_backup = args.sources
backup_dir = args.output

# SSH arguments are inclusive, they must be used all together
if args.port is None and args.username is None and args.address is None and args.password is None:
    ssh = False
elif args.port is not None or args.username is not None or args.address is not None or args.password is not None:
    terminate(101, "Missing argument : for ssh use all ssh arguments are required")
else:
    ssh = True
    ssh_port = args.port
    ssh_username = args.username
    ssh_address = args.address
    ssh_password = args.password


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
    :param directory: Path of the directory to hash.
    :type directory: str
    :return: hex sha256 hash of the directory.
    """
    write_stdout("Computing hash for " + directory + "...\n")

    hashes = []
    for dir_path, dir_names, file_names in os.walk(directory):
        sha256 = hashlib.sha256()
        for file_name in file_names:
            with open(dir_path + "/" + file_name, 'rb') as f:
                # Process file 4096bytes per 4096bytes so the RAM will not be full
                for block in iter(lambda: f.read(4096), b''):
                    sha256.update(block)
            hashes.append(sha256.hexdigest())
    sha256 = hashlib.sha256()
    for h in hashes:
        sha256.update(h.encode('utf-8'))
    write_stdout("Done !\n")
    return sha256.hexdigest()


def initialisation():
    """
    Check if required directories and files exist and create them if needed.
    """
    write_stdout("Initialisation...\n")

    for directory in dirs_to_backup:
        if not os.path.isdir(directory):
            terminate(100, "No directory " + directory + " to backup !")
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
            with open(hashes_json, 'w') as f:
                f.write('{}')
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
                    f.write('{}')
            except Exception as error:
                terminate(error.args[0], str(error))
    write_stdout("Done !\n")


def local_backup(directory: str, new_hash: str):
    """
    Backup locally to the backup_dir.
    :param directory: Path of the directory to backup.
    :type directory: str
    :param new_hash: The hash of the directory to backup.
    :type new_hash: str
    """
    output_filename = os.path.basename(directory)
    write_stdout("Local backup for " + directory + " in progress...\n")
    try:
        to_tar_gz(directory, backup_dir + "/" + output_filename)
        write_stdout("Done !\n")
        update_json(directory, new_hash)
    except Exception as error:
        terminate(error.args[0], str(error))


def distant_backup(directory: str, new_hash: str):
    """
    Backup on distant server to the backup_dir by ssh.
    :param directory: Path of the directory to backup.
    :type directory: str
    :param new_hash: The hash of the directory to backup.
    :type new_hash: str
    """
    print("coming soon !")


def update_json(directory: str, new_hash: str):
    """
    Update the hashes_json with directory as key and new_hash as value.
    :param directory: Path of the backed up directory.
    :type directory: str
    :param new_hash: The hash of the new backed up directory.
    :type new_hash: str
    """
    write_stdout("Updating entries...\n")
    try:
        with open(hashes_json, 'r+') as f:
            data = json.load(f)
            data[directory] = new_hash
            # Rewrite the new hashes_json
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        write_stdout("Done !\n")
    except Exception as error:
        terminate(error.args[0], str(error))


def check_for_changes(directory: str):
    """
    Compare hash in hashes_json and the return of get_directory_hash for a given directory.
    :param directory: The directory to check and eventually backup.
    :type directory: str
    :return result: result['hash'] contains the new hash.
    :return None: If the hashes are equal, no need to backup.
    """

    # I use a dictionary as return for more readability
    result = {'hash': get_directory_hash(directory)}

    with open(hashes_json, 'r') as f:
        data = json.load(f)

    write_stdout("computed hash for " + directory + " : " + result['hash'] + "\n")

    if directory in data:
        write_stdout("founded  hash for " + directory + " : " + data[directory] + " in " + hashes_json + "\n")
        if result['hash'] == data[directory]:
            write_stdout("Same hashes !\n")
            return None
        else:
            write_stdout("Different hashes !\n")
            return result
    else:
        write_stdout("no hash found for " + directory + " in " + hashes_json + "\n")
        write_stdout("New archive !\n")
        return result


initialisation()

for dir_to_backup in dirs_to_backup:
    check_result = check_for_changes(dir_to_backup)
    if check_result is not None:
        local_backup(dir_to_backup, check_result['hash'])
terminate(0, "Work is done !")
