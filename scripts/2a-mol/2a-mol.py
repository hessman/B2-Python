#!/usr/bin/python3

# 2a-mol.py
# Daemon more or less game
# Anthony DOMINGUE
# 28/10/2018

import signal
import sys
import re
import os
from random import randint
from time import sleep

pattern = '^[0-9]*$'  # Regex to check input : any digit
random_number = randint(0, 100)
counter = 0
user_entry = -1  # Init the userEntry with -1 to be sure of entering the while

# Get the directory of the script for game file
game_file = os.path.dirname(os.path.realpath(__file__)) + "/2a-mol.txt"


def goodbye(code: int, message=""):
    """
    Properly exit the script.
    :param code: The exit code or sig.
    :type code: int
    :param message: Optional, the message will be print if str.
    """
    if code is not 0:
        with open(game_file, 'w') as file:
            if isinstance(message, str):
                file.write(message + "\nThe mystery number was " + str(random_number) + ". Goodbye !\n")
            else:
                file.write("Error : " + str(code) + "\nThe mystery number was " + str(random_number) + ". Goodbye !\n")
    sys.exit(code)


signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)


def write_in(text: str):
    """
    Write given text into the game_file.
    :param text: String to write in file.
    :type text: str
    """
    try:
        with open(game_file, 'w') as file:
            file.write(text)
    except Exception as error:
        goodbye(error.args[0], str(error))


def wait_for_response():
    """
    Wait and get the response from the player into the game_file.
    :return: The response of the player, an integer.
    """
    first_line = "y"
    while not re.match(pattern, first_line):
        sleep(3)
        try:
            with open(game_file, 'r') as file:
                first_line = file.readline()
        except Exception as error:
            goodbye(error.args[0], str(error))
    return int(first_line)


write_in("Find the mystery number !")

while int(user_entry) != int(random_number):

    user_entry = wait_for_response()

    if int(random_number) > int(user_entry):
        write_in("more")
    elif int(random_number) < int(user_entry):
        write_in("less")
    counter += 1

write_in("You win\nIn " + str(counter) + " tries !\n")
goodbye(0)
