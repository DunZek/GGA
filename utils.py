def isBinary(str):
    print(str)
    binary = "01"
    if str[-1] != 'b':
        print('No B!')
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
