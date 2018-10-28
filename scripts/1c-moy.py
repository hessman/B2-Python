#!/usr/bin/python3

# 1c-moy.py
# Ask for mark and name then do average and top 5
# Anthony DOMINGUE
# 15/10/2018

import re

pattern = '^[A-z]*\/[0-9]*$'  # Regex to check input
tmp = 0  # Init of tmp variable used to do the average
average = 0
testDict = {}  # Init of the dictionary with names and marks

userEntry = input("Name/Mark:")

while not userEntry == 'q':

    while not re.match(pattern, userEntry):
        userEntry = input("Invalid input, must be ^[A-z]*\/[0-9]*$:")

    # If the input is valid we can safely split string into list   
    name = userEntry.split('/')[0]
    mark = userEntry.split('/')[1]

    """
    Now we can add the mark to the dictionary with name as keys
        __  
       |  | 
       |  |  I want to use dictionary to practice  
       |  |  It is not possible to use the same key twice
       |__|  As we use name as keys we can not use the same name twice
        __   So if there is two John, we must use JohnA JohnB
       |__| 
       
    """
    testDict[name] = mark

    userEntry = input("Name/Mark:")

# Check if the user gave us at least one couple
if len(testDict) > 0:
    # When we have all we process the average
    for name in testDict:
        tmp += int(testDict[name])
    average = tmp / len(testDict)
    print("Average is : ", average)

    """
    Here we sort the dictionary (testDict) to order the values (key=testDict.__getitem__)
    by descending order (reverse=True). It give use a list of names, and so keys,
    ordered by the value assigned to the keys in the dictionary
    """
    names = sorted(testDict, key=testDict.__getitem__, reverse=True)
    i = 0

    # Show the top 5
    for name in names:
        if i > 4:
            break
        # Here we show the rank with i+1, the name from the list and the value from the dictionary with the name as keys
        print("#", i + 1, " ", name, " with ", testDict[name])
        i += 1
else:
    print("Ciao")
