"""
TODO: Give us our daily IT schedule
TODO: Give us our due dates
TODO: Remind holidays/no schools/important days
TODO: Remind people to get sleep
"""
import discord
import os
from keep_alive import keep_alive

client = discord.Client()


# Obtain JSON data
import json
with open('meta.json') as f:
    meta = json.load(f)
with open('messages.json') as f:
    messages = json.load(f)
# with open("schedule.json") as f:
#     schedule = json.load(f)


@client.event
async def on_ready():
    print(f'{client.user} SASUGA DUNCAN-SAMA!')

    test_general = client.get_channel(meta['Test']['channels']['general'])
    await test_general.send("NYA!!!  ( ⓛ ω ⓛ *)")


# Runs Client using bot token
# from dotenv import load_dotenv
# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = os.environ['DISCORD_TOKEN']
client.run(TOKEN)
