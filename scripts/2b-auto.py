#!/usr/bin/python3

# 2b-auto.py
# Daemon more or less player
# Anthony DOMINGUE
# 28/10/2018

import re
import signal
import sys
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


def goodbye(sig="", frame=""):
    """
    Function to properly exit the script
    """
    file = open(game_file, 'w')
    file.write("Player quit after " + str(counter) + " tries. Goodbye !")
    file.close()
    sys.exit(0)


signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)


def write_in():
    """
    Function to write random_number into the game file
    """
    file = open(game_file, 'w')
    file.write(str(random_number))
    file.close()


def choose_random():
    """
    Function to get a random number between min_limit and max_limit
    :return: A random number between min and max value
    """
    return randint(min_limit, max_limit)


def wait_for_response():
    """
    Function to wait and get the response from the player into the game file
    :return: The response of the player, an integer
    """
    first_line = ""
    while re.match(pattern, first_line):
        sleep(3)
        file = open(game_file, 'r')
        first_line = file.readline()
        file.close()
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

sys.exit(0)
