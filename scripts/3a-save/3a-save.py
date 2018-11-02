#!/usr/bin/python3

# 3a-save.py
# Backup tool
# Anthony DOMINGUE
# 31/10/2018

import tarfile
import shutil
import sys
import os

backup_dir = "./data"
backup_tmp_dir = "./data/.tmp"
config_dir = "./data/.config"

dir_to_backup = "./things"

output_filename = os.path.basename(dir_to_backup)


def to_tar_gz(source, output):
    """
    Function to compress the source directory in tar.gz into the output directory
    :param source: Path to the directory to compress
    :param output: Path to the output of the archive
    """
    with tarfile.open(output, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))


def get_directory_checksum(directory):
    """
    Function to get a SHA256 hash of the whole given directory
    :return: str sha256 hash of the directory
    """
    print(directory)
    # TODO : Recursive checksum of all files in the directory


def initialisation():
    """
    Function to check if required directories exist and create them if needed
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
    if not os.path.exists(backup_tmp_dir):
        try:
            os.makedirs(backup_tmp_dir)
        except Exception as error:
            sys.stderr.write(str(error) + "\nExiting !\n")
            sys.exit(2)
    if not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir)
        except Exception as error:
            sys.stderr.write(str(error) + "\nExiting !\n")
            sys.exit(2)
    sys.stdout.write("Done !\n")


def local_backup():
    """
    Function to backup locally
    """
    sys.stdout.write("Local backup to temporary directory...\n")
    try:
        to_tar_gz(dir_to_backup, backup_tmp_dir + "/" + output_filename)
    except Exception as error:
        sys.stderr.write(str(error) + "\nExiting !\n")
        sys.exit(3)
    sys.stdout.write("Done !\n")
    # TODO : Write checksum into .config/hashes.json to compare without extract


def compare_hash(directory):
    """
    Function to compare hash in hashes.json and return of get_directory_checksum for a given directory
    :param directory: Directory to checksum
    :return: True if same
    """
    print(directory)
    # TODO : Finish this function


initialisation()
local_backup()
if not 1:  # TODO : Write a good condition
    sys.stdout.write("Different checksum, moving...\n")
    try:
        shutil.move(backup_tmp_dir + "/" + output_filename, backup_dir + "/" + output_filename)
        sys.stdout.write("Done !\n")
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(str(e) + "\nExiting...\n")
        sys.exit(5)
else:
    sys.stdout.write("Same checksum, erasing temporary file...\n")
    try:
        os.remove(backup_tmp_dir + "/" + output_filename)
        sys.stdout.write("Done !\n")
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(str(e) + "\nExiting...\n")
        sys.exit(6)
