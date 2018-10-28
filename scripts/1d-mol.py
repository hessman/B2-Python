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
randomNumber = randint(0, 100)
counter = 0
userEntry = -1  # Init the userEntry with -1 to be sure of entering the while


def goodbye(sig="", frame=""):
    """
    function to properly exit the script
    """
    print("La solution était :", randomNumber, ". Aurevoir")
    sys.exit(0)


signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)

while not int(userEntry) == int(randomNumber):

    userEntry = input("What is the mystery number :")

    while not re.match(pattern, userEntry):
        print("Invalid input, must be ^[0-9q]*$")
        userEntry = input("What is the mystery number :")

    if str(userEntry) == 'q':
        goodbye()

    if int(randomNumber) > int(userEntry):
        print("more")
    elif int(randomNumber) < int(userEntry):
        print("less")
    counter += 1

print("You win in ", counter, " tries !")
sys.exit(0)
