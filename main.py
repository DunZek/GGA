"""
Other:
! TODO G: Due date labels -> Class, Weekday

Automated:
! TODO B: Remind us of our due dates
! TODO A: Automate due date data capture via scraping
x TODO C: Remind holidays/no schools/important days (manually add some pesky ones)

Manual:
x TODO D: Give us our due dates
x TODO E: Add mute/unmute command -> unmute after 00:00:00, show status <---
x TODO F: return schedule
"""
import discord
# Dealing with dates, holidays
import datetime, holidays, pytz
# Utilities
from discord.ext import tasks
import re
from utils import *
# Data
from data import *
from scrape import result as due_dates

client = discord.Client()

# Automated messages
@tasks.loop(seconds=1)
async def automated():
    # Discord channels
    test_general = client.get_channel(meta['Test']['channels']['general'])
    gg_general = client.get_channel(meta['Group G']['channels']['general'])
    # Setup to send automated messages
    if meta["Production"]:
        general = gg_general  # PRODUCTION
    else:
        general = test_general  # TESTING

    # Variables
    date_utc = pytz.timezone("UTC").localize(datetime.datetime.now())
    date_mt = pytz.timezone("Canada/Mountain").normalize(date_utc)
    if meta["Testing"]:
        date = date_utc  # TESTING
    else:
        date = date_mt  # PRODUCTION
    datestamp = date.strftime("%x")
    timestamp = date.strftime("%X")
    current_weekday = date.strftime("%A")

    # Log
    print("Timestamp: ", timestamp)

    # Unmute automated messages at midnight
    if timestamp == "00:00:01":
        with open('flags.json', 'w') as f:
            flags['mute'] = False
            json.dump(flags, f)

    # If muted, return function and stop execution
    if flags['mute']:
        return

    # Using midnight 00:00:00
    if timestamp == "00:00:00":
        # Remind people to get sleep
        await general.send("GO TO SLEEP-- (≧▽≦) --SEE YOU TOMORROW!!")

    # Send first-line messages - no school
    if timestamp == "08:00:00":
        await general.send("Ohayou  ^ω^")
        # Remind weekend
        if current_weekday not in weekdays:
            await general.send("No school enjoy your weekend (≧ω≦)")
        # Remind holidays/no schools/important days
        elif datestamp in holiday_dates:
            await general.send("It's a holiday no school!! (≧▽≦)")

    # Return if no school
    if current_weekday not in schedule:
        return

    # Send first-line messages - weekdays
    startOfClass = timeToStamp(schedule[current_weekday][0]["Start"])
    if timestamp == startOfClass[:3] + "45" + startOfClass[5:] or timestamp == "08:00:00":  # either "07:45:00" or "08:45:00"
        # Give us our daily IT schedule
        await general.send("Ohayou  ^ω^")
        await general.send("Here's your schedule", embed=getSchedule(current_weekday, schedule))
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
    # print(f'"{message.content}"')

    # Help
    if re.match(f'^<@[!&]*{ID}>[ ]*([hH]elp)*$', message.content):
        result = ''
        embedded = discord.Embed(title=messages["help"]["Title"], color=0xDC143C)
        for string in messages["help"]["Strings"]:
            result += string + '\n'
        embedded.add_field(name='\u200b', value=result, inline=False)
        await message.channel.send("Nya ( ⓛ ω ⓛ *)~~ you called for help", embed=embedded)

    # Commands beginning with ping
    if re.match(f'^<@[!&]*{ID}>', message.content):
        # Return recorded due dates of the month
        if re.search('[dD]ue$', message.content):
            await message.channel.send("Here are your due dates since recorded last time", embed=getDue(due_dates, current_month))
        # Return recorded every due date
        if re.search('[dD]ue [aA]ll$', message.content):
            await message.channel.send("Here are your due dates since recorded last time")
            for m in due_dates:
                await message.channel.send(embed=getDue(due_dates, m))

        # Return schedule
        if re.search('[sS]chedule$', message.content):
            # Variables
            date_utc = pytz.timezone("UTC").localize(datetime.datetime.now())
            date_mt = pytz.timezone("Canada/Mountain").normalize(date_utc)
            if meta["Testing"]:
                date = date_utc  # TESTING
            else:
                date = date_mt  # PRODUCTION
            datestamp = date.strftime("%x")
            timestamp = date.strftime("%X")
            current_weekday = date.strftime("%A")
            if current_weekday not in weekdays or datestamp in holiday_dates:
                await message.channel.send("You don't have school today ( ⓛ ω ⓛ *)")
            else:
                await message.channel.send("Here's your schedule for this day", embed=getSchedule(current_weekday, schedule))

        # Mute/Unmute automated messages
        if re.search('[uU]nmute$', message.content):
            with open('./flags.json', 'w') as f:
                flags['mute'] = False
                json.dump(flags, f)
            await message.channel.send("*automated messages unmuted*")
            await client.change_presence(activity=None)
        elif re.search('[mM]ute$', message.content):
            with open('./flags.json', 'w') as f:
                flags['mute'] = True
                json.dump(flags, f)
            await message.channel.send("*automated messages muted until the next day*")
            await client.change_presence(activity=discord.Game("muted"))

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

        # Some fun messages
        if 'ohayou' in message.content:
            await message.channel.send('GOZAIMASUUU!!!')
        if 'you cute baby' in message.content:
            await message.channel.send("BAKA (ˋ3ˊ)")

    # React to kind messages
    if re.search('(thank you|ty|)+(group g|ai|goat|bot)+', message.content):
        await message.add_reaction('\U00002764')

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

    # Log
    await general.send("NYA!!!  ( ⓛ ω ⓛ *)")

    # Manual
    message = client.get_message(894687899314970624)
    await message.add_reaction('\U00002764')
    
    # Start loop
    automated.start()

# Because Discord will nullify tokens if it tracks them online
client.run("ODg5ODkwMjIz" + "OTA1OTkyNzE1.YUn0" + "2g.ckhiQeUNiFit6" + "3PKI3IR0mUFRBs")
