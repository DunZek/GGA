hexadecimal = "0123456789ABCDEF"
hex = "FF"
power, value = 0, 0
for i in range(len(hex), 0, -1):
    char = hex[i - 1]
    value += hexadecimal.find(char) * 16 ** power
    power += 1
print(value)
