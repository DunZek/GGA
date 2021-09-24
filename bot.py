# bot.py interface
import discord
import os
from utils import *  # util functions
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Object representing connection to Discord
client = discord.Client()

# Controller -> automated
@client.event
async def on_ready():
    print(f'{client.user} SASUGA DUNCAN-SAMA!')

    channel = client.get_channel(885181132239413272)
    # await channel.send("NYA!!!  ( ⓛ ω ⓛ *)")


# Controller -> channel messages
@client.event
async def on_message(message):
    if message.author == client.user: return
    #print(message.content)

    # Help
    if message.content == "<@!889890223905992715>" or message.content == "<@889890223905992715>":
        await message.channel.send("""
Nya ( ⓛ ω ⓛ *)~~ you called for help

**Binary-to-Decimal**
*Convert given binary number to decimal equivalent*
    `Usage:: /([01]+b)+/`
    `Example::  "110b 001b"  // 6, 9`

**Hexadecimal-to-Decimal**
*Convert given hexadecimal value to decimal equivalent*
    `Usage:: /([0123456789ABCDEF]+h)+/`
    `Example::  "FFh 10h"  // 15, 16`
            """)

    # Fun messages
    if message.content == 'ohayou':
        await message.channel.send("GOZAIMASUUU!!!")
    if message.content == 'you cute baby':
        await message.channel.send("BAKA (ˋ3ˊ)")

    # Convert binary
    if isBinary(message.content.split(' ')[0]) and message.content.split(' ')[0][-1] == 'b':
        returned = ""
        for word in message.content.split(' '):
            if isBinary(word) and word[-1] == 'b':
                value, power, = 0, 0
                for i in range(len(word) - 1, 0, -1):
                    if word[i - 1] == "1":
                        value += 2 ** power
                    power += 1
                returned += str(value) + " "
        await message.channel.send("Praise the Omnissiah: " + returned)

    # Convert hexadecimal
    if isHexadecimal(message.content.split(' ')[0]) and message.content.split(' ')[0][-1] == 'h':
        hexadecimal = "0123456789ABCDEF"
        returned = ""
        for word in message.content.split(' '):
            if isHexadecimal(word) and word[-1] == 'h':
                power, value = 0, 0
                for i in range(len(word) - 1, 0, -1):
                    char = word[i - 1]
                    value += hexadecimal.find(char) * 16 ** power
                    power += 1
                returned += str(value) + " "
        await message.channel.send("Praise the Omnissiah: " + returned)

# Runs Client using bot token
client.run(TOKEN)
