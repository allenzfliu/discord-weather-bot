#!/usr/bin/python3
import os
import discord

from dotenv import load_dotenv
load_dotenv();
TOKEN = os.getenv('DISCORD_BOT_TOKEN_DO_NOT_SHARE_EVER');
OPEN_CHANNEL = os.getenv('OPEN_CHANNEL');
MESSAGE_HEADER = "w! ";
DEBUG = True;

def debug(message):
    if (DEBUG):
        print(message);

intents = discord.Intents.default();
intents.message_content = True;
client = discord.Client(intents=intents);

@client.event
async def on_ready():
    debug("Hello burgle!");
    # channel = client.get_channel(1254693534863327314);
    # await channel.send('Hello burgle!')

@client.event
async def on_message(message):
    debug(f'{message.author}: {message.content}');
    if (message.author == client.user):
        return;
    
    #first check if message starts with header
    if (message.content.lower()[0:3] == MESSAGE_HEADER):
        if (message.content.lower() == "w! status"):
            # send a bot status message
            await message.channel.send("Weather bot is running. Fetching weather.gov API status...");
        else:
            await message.channel.send("Unknown weather bot command.");

client.run(TOKEN);