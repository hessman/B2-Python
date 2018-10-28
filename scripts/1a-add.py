#!/usr/bin/python3

# 1a-add.py
# Simple addition script
# Anthony DOMINGUE
# 15/10/2018

import re

pattern = '^[0-9]*$'  # Regex to check input : any digit

nb1 = input("Enter number 1:")
nb2 = input("Enter number 2:")

while not re.match(pattern, nb1) or not re.match(pattern, nb2):
    print("Invalid input, must be ^[0-9]*$")
    nb1 = input("Enter number 1:")
    nb2 = input("Enter number 2:")

result = int(nb1) + int(nb2)
print(result)
