#!/usr/bin/python3

# 1d-mol.py
# Simple more or less game
# Anthony DOMINGUE
# 15/10/2018

import re
import signal
import sys
from random import randint

pattern = '^[0-9q]*$'  # Regex to check input : any digit or q
random_number = randint(0, 100)
counter = 0
user_entry = -1  # Init the userEntry with -1 to be sure of entering the while


def goodbye(sig="", frame=""):
    """
    Function to properly exit the script
    """
    print("The mystery number was :", random_number, ". Goodbye !")
    sys.exit(0)


signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)

while int(user_entry) != int(random_number):

    user_entry = input("What is the mystery number ? :")

    while not re.match(pattern, user_entry):
        print("Invalid input, must be ^[0-9q]*$")
        user_entry = input("What is the mystery number :")

    if str(user_entry) == 'q':
        goodbye()

    if int(random_number) > int(user_entry):
        print("more")
    elif int(random_number) < int(user_entry):
        print("less")
    counter += 1

print("You win in ", counter, " tries !")
sys.exit(0)
