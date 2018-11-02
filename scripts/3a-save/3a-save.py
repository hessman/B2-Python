#!/usr/bin/python3

# 3a-save.py
# Backup tool
# Anthony DOMINGUE
# 31/10/2018

# TODO : SIGINT and SIGTERM
# TODO : exit function ?

import tarfile
import hashlib
import json
import sys
import os

backup_dir = "./data"
config_dir = "./data/.config"
hashes_json = config_dir + "/hashes.json"

dir_to_backup = "./things"
output_filename = os.path.basename(dir_to_backup)


def to_tar_gz(source, output):
    """
    Function to compress the source in tar.gz into the output
    :param source: Path of the directory to compress
    :param output: Path of the output of the archive
    """
    with tarfile.open(output, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))


def get_directory_checksum(directory):
    """
    Give a SHA256 checksum of the whole given directory by recursively hash the directory and hash the array of hashes
    :param directory: Path of the directory to checksum
    :return: hex sha256 hash of the directory
    """
    sys.stdout.write("Computing hashes...\n")
    hashes = []
    for dir_path, dir_names, file_names in os.walk(directory):
        sha256 = hashlib.sha256()
        for file_name in file_names:
            with open(dir_path + "/" + file_name, 'rb') as f:
                for block in iter(lambda: f.read(4096), b''):
                    sha256.update(block)
            hashes.append(sha256.hexdigest())
    sha256 = hashlib.sha256()
    for h in hashes:
        sha256.update(h.encode('utf-8'))
    sys.stdout.write("Done !\n")
    return sha256.hexdigest()


def initialisation():
    """
    Function to check if required directories and files exist and create them if needed
    """
    sys.stdout.write("Initialisation...\n")
    if not os.path.isdir(dir_to_backup):
        sys.stderr.write("No directory to backup...\nExiting !\n")
        sys.exit(1)
    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
        except Exception as error:
            sys.stderr.write(str(error) + "\nExiting !\n")
            sys.exit(2)
    if not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir)
        except Exception as error:
            sys.stderr.write(str(error) + "\nExiting !\n")
            sys.exit(2)
    if not os.path.exists(hashes_json):
        try:
            with open(hashes_json, 'a+') as f:
                f.write('{}')
        except Exception as error:
            sys.stderr.write(str(error) + "\nExiting !\n")
            sys.exit(2)
    sys.stdout.write("Done !\n")


def local_backup(directory, new_hash):
    """
    Backup locally to the backup_dir
    :param directory: Path of the directory to backup
    :param new_hash: The hash of the directory to backup
    """
    sys.stdout.write("Local backup in progress...\n")
    try:
        to_tar_gz(directory, backup_dir + "/" + output_filename)
        sys.stdout.write("Done !\n")
        update_json(directory, new_hash)
    except Exception as error:
        sys.stderr.write(str(error) + "\nExiting !\n")
        sys.exit(3)


def update_json(directory, new_hash):
    """
    Update the hashes_json with directory as key and new_hash as value.
    :param directory: Path of the directory backed up
    :param new_hash: The hash of the new backed up directory
    """
    sys.stdout.write("Updating entries...\n")
    try:
        with open(hashes_json, 'r+') as f:
            data = json.load(f)
            data[directory] = new_hash
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        print(data)
        sys.stdout.write("Done !\n")
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(str(e) + "\nExiting...\n")
        sys.exit(5)


def check(directory):
    """
    Compare hash in hashes_json and the return of get_directory_checksum for a given directory.
    :param directory: The directory to check and eventually backup.
    """
    new_hash = get_directory_checksum(directory)
    with open(hashes_json) as f:
        data = json.load(f)

    print("founded  hash for " + directory + " : " + data[directory] + " in " + hashes_json)
    print("computed hash for " + directory + " : " + new_hash)
    if directory in data:
        if new_hash == data[directory]:
            sys.stdout.write("Same checksum, exiting...\n")
            sys.exit(0)
        else:
            sys.stdout.write("Different checksum !\n")
            local_backup(directory, new_hash)
    else:
        sys.stdout.write("New archive !\n")
        local_backup(directory, new_hash)


initialisation()
check(dir_to_backup)
