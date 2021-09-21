# bot.py interface
import discord
import os
from applications import schedule  # functionalities
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
    await channel.send("NYA!!!  ( ⓛ ω ⓛ *)")


# Controller -> channel messages
@client.event
async def on_message(message):
    if message.author == client.user: return

    # Fun messages
    if message.content == 'ohayou':
        await message.channel.send("GOZAIMASUUU!!!")
    if message.content == 'you cute baby':
        await message.channel.send("BAKA (ˋ3ˊ)")



# Runs Client using bot token
client.run(TOKEN)
