import re, discord

# Binary to Decimal
def BtD(words):
    result = ""
    for word in words:
        if isBinary(word):
            value, power, = 0, 0
            for i in range(len(word), 0, -1):
                if word[i - 1] == "1":
                    value += 2 ** power
                power += 1
            result += str(value) + " "
    return result

# BtD helper function
def isBinary(str):
    binary = "01"
    for char in str:
        if char not in binary:
            return False
    return True

# Hexadecimal to Decimal
def HtD(words):
    hexadecimal = "0123456789ABCDEF"
    result = ""
    for word in words:
        if isHexadecimal(word):
            power, value = 0, 0
            for i in range(len(word), 0, -1):
                char = word[i - 1]
                value += hexadecimal.find(char) * 16 ** power
                power += 1
            result += str(value) + " "
    return result

# HtD helper function
def isHexadecimal(str):
    hexadecimal = "0123456789ABCDEF"
    for char in str:
        if char not in hexadecimal:
            return False
    return True

# Creating a timestamp -> strftime(%X) from "\d{1-2}:\d\d [AP]M"
def timeToStamp(time):
    elements = re.split(':| ', time)
    hour = 0 if elements[2] == 'AM' else 12
    return f'{str(hour + int(elements[0])).zfill(2)}:{str(elements[1])}:00'

# Generate schedule
def getSchedule(weekday, schedule):
    embedded = discord.Embed(title=weekday, color=0xDC143C)
    for Class in schedule[weekday]:
        value = f'**{Class["Class"]}** \n'
        value += f'Start - {Class["Start"]} \n'
        value += f'Where - {Class["Where"]} \n'
        value += f'End - {Class["End"]} \n'
        embedded.add_field(name='\u200b', value=value, inline=False)
    return embedded

# Get due dates
def getDue(dictionary, name):
    # Get month
    month = dictionary[name]
    # Initialized with title
    embedded = discord.Embed(title=name, color=0xDC143C)
    # Appending the date
    for date in month:
        string = f'**{name[:3]} {ordinalSuffix(date)}, 2021**\n'
        # Appending the assignments
        for assignment in month[date]:
            string += f'{month[date][assignment]} **<<** {assignment}\n'
        # Adding the field
        embedded.add_field(name='\u200b', value=string, inline=False)
    return embedded

# Ordinal suffixing
def ordinalSuffix(number):
    # Convert to string if given integer
    number = str(number) if type(number) == int else number
    ones = number[-1]
    if ones == '1':
        number += "st"
    elif ones == '2':
        number += "nd"
    elif ones == '3':
        number += 'rd'
    else:
        number += "th"
    return number

# -- dev. tests --
# print(HtD(["FF"]))
# print(BtD(["1"]))
