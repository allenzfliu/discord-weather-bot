#!/usr/bin/python3
import os
import discord
from dotenv import load_dotenv
import requests

load_dotenv();
TOKEN = os.getenv('DISCORD_BOT_TOKEN_DO_NOT_SHARE_EVER');
OPEN_CHANNEL = os.getenv('OPEN_CHANNEL');
MESSAGE_HEADER = "w! ";
DEBUG = True;

if (DEBUG):
    def debug(message):
        print(message)
else:
    def debug(message):
        pass;

def weather_api_fetch(url):
    response = requests.get(url);
    print(response.status_code);
    return response.json();

def main():
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
                url = "https://api.weather.gov/alerts/types";
                response = requests.get(url);
                if (response.status_code == 200):
                    await message.channel.send("Received 200 OK from API.");
                else:
                    await message.channel.send("Did not receive expected error code from API! Something has gone terribly wrong!");
                    await message.channel.send("The actual code we received was: " + str(response.status_code));
            else:
                await message.channel.send("Unknown weather bot command.");

    client.run(TOKEN);

if (__name__ == "__main__"):
    main();