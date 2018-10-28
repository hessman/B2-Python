#!/usr/bin/python3

# 1b-dic.py
# Ask for name
# Anthony DOMINGUE
# 15/10/2018

import re

pattern = '^[A-z]*$'  # Regex to check input : any amount of letter, caps or not
userEntry = ''
namesList = []

while not userEntry == 'q':

    userEntry = input("Enter a name :")

    while not re.match(pattern, userEntry):
        print("Invalid input, must be ^[A-z]*$")
        userEntry = input("Enter a name :")

    if not userEntry == 'q':
        namesList.append(userEntry)

sorted(namesList)  # We sort the list (by default alphabetically)
print(namesList)
