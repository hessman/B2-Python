#!/usr/bin/python3

# 1b-dic.py
# Ask for name
# Anthony DOMINGUE
# 15/10/2018

import re

pattern = '^[A-z]*$'  # Regex to check input : any amount of letter, caps or not
user_entry = ''
names_list = []

while user_entry != 'q':

    user_entry = input("Enter a name :")

    while not re.match(pattern, user_entry):
        print("Invalid input, must be ^[A-z]*$")
        user_entry = input("Enter a name :")

    if not user_entry == 'q':
        names_list.append(user_entry)

sorted(names_list)  # We sort the list (by default alphabetically)
print(names_list)
