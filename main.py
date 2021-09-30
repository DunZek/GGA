"""
TODO: Give us our daily IT schedule ✓
! TODO: Give us our due dates -- hard to automate 
TODO: Remind holidays/no schools/important days ✓ (NOT all)
TODO: Remind people to get sleep ✓
! TODO: Info + Help
"""
import discord
import os
from datetime import datetime
import holidays
import pytz
import time
from utils import *
import re
from keep_alive import keep_alive
from discord.ext import commands, tasks
from itertools import cycle

client = discord.Client()

# https://skidee.medium.com/host-a-discord-bot-24-7-online-for-free-4f30cd8ba78e
status = cycle(['( ⓛ ω ⓛ *)', '(≧▽≦)'])
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# Obtain JSON data
import json
with open('meta.json') as f:
    meta = json.load(f)
with open('messages.json') as f:
    messages = json.load(f)
with open("schedule.json") as f:
    schedule = json.load(f)
# Data - on_ready
weekdays = dict.keys(schedule)
holiday_dates = [holiday[0].strftime("%x") for holiday in holidays.Canada(years=2021).items()]
holiday_names = [holiday[1] for holiday in holidays.Canada(years=2021).items()]
# Data - on_message
ID_PC = meta["GGA"]["ID_PC"]
ID_MB = meta["GGA"]["ID_MB"]
ID = str(meta["GGA"]["ID"])

# Start
@client.event
async def on_ready():
    print(f'{client.user} SASUGA DUNCAN-SAMA!')

    # Discord channels
    test_general = client.get_channel(meta['Test']['channels']['general'])
    gg_general = client.get_channel(meta['Group G']['channels']['general'])

    # Variables
    general = test_general  # for use

    # Online
    await test_general.send("NYA!!!  ( ⓛ ω ⓛ *)")

    # Automated daily messages
    while True:
        # keep_alive
        change_status.start()
        # Variables
        date_utc = pytz.timezone("UTC").localize(datetime.now())
        date_mt = pytz.timezone("Canada/Mountain").normalize(date_utc)
        date = date_mt
        datestamp = date.strftime("%x")
        timestamp = date.strftime("%X")
        current_weekday = date.strftime("%A")

        # Remind people to get sleep
        if timestamp == "21:00:00":
            await general.send("GO TO SLEEP (≧▽≦) SEE YOU TOMORROW!!")
            time.sleep(1)
        
        # At 7, send first-line messages
        if timestamp == "19:00:50":
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
            time.sleep(1)

        # Remind...
        today = schedule[current_weekday]
        for i in range(len(today)):
            Class = today[i]
            # a fair well at the end of the day
            if timestamp == timeToStamp(Class["End"]) and i + 1 == len(today):
                await general.send("Classes have ended. Have a good afternoon! (≧▽≦)")
                time.sleep(1)
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
                time.sleep(1)

# User messages
@client.event
async def on_message(message):
    if message.author == client.user: return
    print(message.content)

    # Help - TODO
    if re.match(f'^<@[!&]{ID}>$', message.content) is not None:
        embedded = discord.Embed(title=current_weekday, color=0xDC143C)

        await message.channel.send("Nya ( ⓛ ω ⓛ *)~~ you called for help", embed=embedded)

    # Fun messages
    if re.match(f'<@[!&]{ID}>', message.content) is not None:
        if 'ohayou' in message.content:
            await message.channel.send('GOZAIMASUUU!!!')
        if 'you cute baby' in message.content:
            await message.channel.send("BAKA (ˋ3ˊ)")

    # Binary to Decimal
    flag_start = isBinary(message.content.split(' ')[0])
    flag_end = message.content.split(' ')[0][-1] == 'b'
    if flag_start and flag_end:
        result = f"Praise the OwO-nissiah: **{str(BtD(message.content.split(' ')))}**"
        await message.channel.send(result)

    # Hexadecimal to Decimal
    flag_start = isHexadecimal(message.content.split(' ')[0])
    flag_end = message.content.split(' ')[0][-1] == 'h'
    if flag_start and flag_end:
        result = f"Praise the OwO-nissiah: **{str(HtD(message.content.split(' ')))}**"
        await message.channel.send(result)

# keep_alive.py
keep_alive()
# from dotenv import load_dotenv
# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
client.run(os.environ['DISCORD_TOKEN'])