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

# a helper function
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

# a helper function
def isHexadecimal(str):
    hexadecimal = "0123456789ABCDEF"
    for char in str:
        if char not in hexadecimal:
            return False
    return True

# Creating a timestamp -> strftime(%X) from "\d{1-2}:\d\d [AP]M"
def timeToStamp(time):
    import re
    elements = re.split(':| ', time)
    hour = 0 if elements[2] == 'AM' else 12
    return f'{str(hour + int(elements[0])).zfill(2)}:{str(elements[1])}:00'


# -- dev. tests --
# print(HtD(["FF"]))
# print(BtD(["1"]))
