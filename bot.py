#!/usr/bin/python3
import os
import discord
from dotenv import load_dotenv
import requests
import datetime


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
            if (message.content.lower() == "w! help"):
                help_message = "## Burgle Weather Bot Help";
                help_message += "\n-# Bot prefix is `w! ` (includes space)."
                help_message += "\n* **w! help**- Prints this help message."
                help_message += "\n* **w! status**- Prints a bot and weather API status info."
                help_message += "\n* **w! forecast today <location>**- Prints today's forecast, hour by hour."
                help_message += "\n* **w! forecast <location>**- Prints a 14 day forecast of high temperatures, low temperatures, and precipitation info."
                # help_message += "\n* **w! add location <location>**- Adds a location."
                await message.channel.send(help_message);
            elif (message.content.lower() == "w! status"):
                # send a bot status message
                await message.channel.send("Weather bot is running. Fetching weather.gov API status...");
                url = "https://api.weather.gov/alerts/types";
                response = requests.get(url);
                if (response.status_code == 200):
                    await message.channel.send("Received 200 OK from API.");
                else:
                    await message.channel.send("Did not receive expected error code from API! Something has gone terribly wrong!");
                    await message.channel.send("The actual code we received was: " + str(response.status_code));
            elif (message.content.lower() == "w! forecast today"):
                # to keep it shrimple, we'll use the coords given by the user.
                # using 38, -77 as a test coord
                lat=38;
                long=-77;
                url = "https://api.weather.gov/points/" + str(lat) + "," + str(long);
                properties = weather_api_fetch(url)["properties"];
                debug(properties);
                gridId = properties["gridId"];
                gridX = properties["gridX"];
                gridY = properties["gridY"];
                forecast_url = properties["forecastHourly"];
                forecast = weather_api_fetch(forecast_url)["properties"];
                this_hour = forecast["periods"][0];
                localized_time = datetime.datetime.fromisoformat(this_hour["startTime"]).strftime("%I:%M%p on %B %d, %Y")

                await message.channel.send(f"Forecast for {localized_time}: Temperature of {this_hour['temperature']}*{this_hour['temperatureUnit']}")
            else:
                await message.channel.send("Unknown weather bot command.");

    client.run(TOKEN);

if (__name__ == "__main__"):
    main();