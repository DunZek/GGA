"""
Core:

Automated:
! TODO #2: Give us our due dates -- hard to automate
x TODO #3: Remind holidays/no schools/important days (manually add some pesky ones)

Manual:
! TODO #6: Add mute/unmute command -> unmute after 00:00:00, show status <---
! TODO #7: return schedule
"""
import discord
# Dealing with dates, holidays, timezones
import datetime, holidays, pytz
# Utilities
from discord.ext import tasks
import re
from utils import *
# Data
from data import *

client = discord.Client()

# Automated messages
@tasks.loop(seconds=1)
async def automated():
    # Discord channels
    test_general = client.get_channel(meta['Test']['channels']['general'])
    gg_general = client.get_channel(meta['Group G']['channels']['general'])
    # general = test_general  # TESTING
    general = gg_general  # PRODUCTION

    # Variables
    date_utc = pytz.timezone("UTC").localize(datetime.datetime.now())
    date_mt = pytz.timezone("Canada/Mountain").normalize(date_utc)
    date = date_mt
    datestamp = date.strftime("%x")
    timestamp = date.strftime("%X")
    current_weekday = date.strftime("%A")

    # Unmute automated messages at midnight
    if timestamp == "00:00:00":
        with open('flags.json', 'w') as f:
            flags['mute'] = False
            json.dump(flags, f)

    # If muted, return function and stop execution
    if flags['mute']:
        return

    # Log
    # print(timestamp)

    # Using midnight 00:00:00
    if timestamp == "00:00:00":
        # Remind people to get sleep
        await general.send("GO TO SLEEP-- (≧▽≦) --SEE YOU TOMORROW!!")

    # Send first-line messages
    startOfClass = timeToStamp(schedule[current_weekday][0]["Start"])
    if timestamp == startOfClass[:3] + "45" + startOfClass[5:] or timestamp == "08:00:00":  # either "07:45:00" or "08:45:00"
        await general.send("Ohayou  ^ω^")
        # Remind weekend
        if current_weekday not in weekdays:
            await general.send("No school enjoy your weekend (≧ω≦)")
        # Remind holidays/no schools/important days
        elif datestamp in holiday_dates:
            await general.send("It's a holiday no school!! (≧▽≦)")
        # Give us our daily IT schedule
        else:
            embedded = discord.Embed(title=current_weekday, color=0xDC143C)
            for Class in schedule[current_weekday]:
                value = f'**{Class["Class"]}** \n'
                value += f'Start - {Class["Start"]} \n'
                value += f'Where - {Class["Where"]} \n'
                value += f'End - {Class["End"]} \n'
                embedded.add_field(name='\u200b', value=value, inline=False)
            await general.send("Here's your schedule", embed=embedded)
            await general.send("≧ω≦ do your best :heart:")

    # Remind during class days (non-weekends and non-holidays)
    if current_weekday in weekdays and datestamp not in holiday_dates:
        today = schedule[current_weekday]
        for i in range(len(today)):
            Class = today[i]
            # a fair well at the end of the day
            if timestamp == timeToStamp(Class["End"]) and i + 1 == len(today):
                await general.send("Classes have ended. Have a good afternoon! (≧▽≦)")

            # or the next class
            elif timestamp == timeToStamp(Class["End"]):
                await general.send("Here's your next class ≧ω≦")
                embedded = discord.Embed(title=current_weekday, color=0xDC143C)
                value = f'**{today[i + 1]["Class"]}** \n'
                value += f'Start - {today[i + 1]["Start"]} \n'
                value += f'Where - {today[i + 1]["Where"]} \n'
                value += f'End - {today[i + 1]["End"]} \n'
                embedded.add_field(name='\u200b', value=value, inline=False)
                await general.send(embed=embedded)


# User messages
@client.event
async def on_message(message):
    if message.author == client.user: return
    print(f'"{message.content}"')

    # Help
    if re.match(f'^<@[!&]*{ID}>[ ]*([hH]elp)*$', message.content) is not None:
        result = ''
        embedded = discord.Embed(title=messages["help"]["Title"], color=0xDC143C)
        for string in messages["help"]["Strings"]:
            result += string + '\n'
        embedded.add_field(name='\u200b', value=result, inline=False)
        await message.channel.send("Nya ( ⓛ ω ⓛ *)~~ you called for help", embed=embedded)

    # Commands beginning with ping
    if re.match(rf'\b<@[!&]*{ID}>', message.content) is not None:
        # Some fun messages
        if 'ohayou' in message.content:
            await message.channel.send('GOZAIMASUUU!!!')
        if 'you cute baby' in message.content:
            await message.channel.send("BAKA (ˋ3ˊ)")

        # Mute/Unmute automated messages
        if 'mute' in message.content:
            with open('flags.json', 'w') as f:
                flags['mute'] = True
                json.dump(flags, f)
            await message.send.channel("*automated messages muted until the next day*")
        elif 'unmute' in message.content:
            with open('flags.json', 'w') as f:
                flags['mute'] = False
                json.dump(flags, f)
            await message.send.channel("*automated messages unmuted*")

        # Binary to Decimal
        flag_start = isBinary(message.content.split(' ')[1])
        flag_end = message.content[-1] == 'b'
        if flag_start and flag_end:
            result = f"Praise the OwO-nissiah: **{str(BtD(message.content.split(' ')))}**"
            await message.channel.send(result)

        # Hexadecimal to Decimal
        flag_start = isHexadecimal(message.content.split(' ')[1])
        flag_end = message.content[-1] == 'h'
        if flag_start and flag_end:
            result = f"Praise the OwO-nissiah: **{str(HtD(message.content.split(' ')))}**"
            await message.channel.send(result)


# Start
@client.event
async def on_ready():
    # Online
    print(f'{client.user} SASUGA DUNCAN-SAMA!')

    # Discord channels
    test_general = client.get_channel(meta['Test']['channels']['general'])
    gg_general = client.get_channel(meta['Group G']['channels']['general'])

    # Variables
    general = test_general  # TESTING
    # general = gg_general  # PRODUCTION

    await general.send("NYA!!!  ( ⓛ ω ⓛ *)")
    # Start loop
    automated.start()

# Because Discord will nullify tokens if it tracks them online
client.run("ODg5ODkwMjIz" + "OTA1OTkyNzE1.YUn0" + "2g.ckhiQeUNiFit6" + "3PKI3IR0mUFRBs")
