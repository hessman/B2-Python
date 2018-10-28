#!/usr/bin/python3

# 2a-mol.py
# Daemon more or less game
# Anthony DOMINGUE
# 28/10/2018

import re
import signal
import sys
import os
from random import randint
from time import sleep

pattern = '^[0-9]*$'  # Regex to check input : any digit
random_number = randint(0, 100)
counter = 0
user_entry = -1  # Init the userEntry with -1 to be sure of entering the while
game_file = os.path.dirname(os.path.realpath(__file__)) + "/2a-mol.txt"  # Get the directory of the script for game file


def goodbye(sig="", frame=""):
    """
    Function to properly exit the script
    """
    write_in("The mystery number was " + str(random_number) + ". Goodbye !")
    sys.exit(0)


signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)


def write_in(text: str):
    """
    Function to write given text into the game file
    :param text: String to write in file
    """
    file = open(game_file, 'w')
    file.write(text)
    file.close()
    

def wait_for_response():
    """
    Function to wait and get the response from the player into the game file
    :return: The response of the player, an integer
    """
    first_line = "y"
    while not re.match(pattern, first_line):
        sleep(3)
        file = open(game_file, 'r')
        first_line = file.readline()
        file.close()
    return int(first_line)


write_in("Find the mystery number !")

while int(user_entry) != int(random_number):

    user_entry = wait_for_response()

    if int(random_number) > int(user_entry):
        write_in("more")
    elif int(random_number) < int(user_entry):
        write_in("less")
    counter += 1

write_in("You win in " + str(counter) + " tries !")
sys.exit(0)
