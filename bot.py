#!/usr/bin/python3
import os
import discord

from dotenv import load_dotenv
load_dotenv();
TOKEN = os.getenv('DISCORD_BOT_TOKEN_DO_NOT_SHARE_EVER');
OPEN_CHANNEL = os.getenv('OPEN_CHANNEL');
DEBUG = True;

def debug(message):
    if (DEBUG):
        print(message);

intents = discord.Intents.default();
intents.message_content = True;
client = discord.Client(intents=intents);

@client.event
async def on_ready():
    channel = client.get_channel(1254693534863327314);
    await channel.send('Hello burgle!');

@client.event
async def on_message(message):
    debug(f'{message.author}: {message.content}');
    if (message.author == client.user):
        return;
    

client.run(TOKEN);