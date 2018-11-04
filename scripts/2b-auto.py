#!/usr/bin/python3

# 2b-auto.py
# Daemon more or less player
# Anthony DOMINGUE
# 28/10/2018

import signal
import sys
import re
import os
from random import randint
from time import sleep

pattern = '^[0-9]*$'  # Regex to check input : any digit
max_limit = 100
min_limit = 0
random_number = randint(min_limit, max_limit)
counter = 0
response = " "  # Init the userEntry with " " to be sure of entering the while

# Get the directory of the script for game file
game_file = os.path.dirname(os.path.realpath(__file__)) + "/2a-mol/2a-mol.txt"


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
                file.write(message + "\nPlayer quit after " + str(counter) + " tries. Goodbye !\n")
            else:
                file.write("Error : " + str(code) + "\nPlayer quit after " + str(counter) + " tries. Goodbye !\n")
    sys.exit(code)


signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)


def write_in():
    """
    Write random_number into the game_file.
    """
    try:
        with open(game_file, 'w') as file:
            file.write(str(random_number))
    except Exception as error:
        goodbye(error.args[0], str(error))


def choose_random():
    """
    Give a random number between min_limit and max_limit.
    :return: An integer between min and max value.
    """
    return randint(min_limit, max_limit)


def wait_for_response():
    """
    Wait and get the response from the player into the game_file.
    :return: The response of the player, an integer.
    """
    first_line = ""
    while re.match(pattern, first_line):
        sleep(3)
        try:
            with open(game_file, 'r') as file:
                first_line = file.readline()
        except Exception as error:
            goodbye(error.args[0], str(error))
    return str(first_line)


write_in()

while str(response) != "You win\n":

    response = wait_for_response()

    if str(response) == "more":
        min_limit = random_number
        random_number = choose_random()
        write_in()
    elif str(response) == "less":
        max_limit = random_number
        random_number = choose_random()
        write_in()
    counter += 1

goodbye(0)
