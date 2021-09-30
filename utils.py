def isBinary(str):
    # print(str)
    binary = "01"
    if str[-1] != 'b':
        # print('No B!')
        return False
    for char in str:
        if char == 'b':
            continue
        elif char not in binary:
            return False
        # if char != "1":
        #     if char != "0":
        #         if str[-1] != 'b':
        #             return False
    return True

def isHexadecimal(str):
    hexadecimal = "0123456789ABCDEF"
    for char in str:
        if char not in hexadecimal and str[-1] != 'h':
            return False
    return True

def timeToStamp(time):
    import re
    elements = re.split(':| ', time)
    hour = 0 if elements[2] == 'AM' else 12
    return f'{str(hour + int(elements[0])).zfill(2)}:{str(elements[1])}:00'

# print(timeToStamp("4:30 PM"))  # 16:30:00
# print(timeToStamp("10:50 AM"))  # 10:50:00
# print(timeToStamp("8:00 AM"))  # 08:00:00