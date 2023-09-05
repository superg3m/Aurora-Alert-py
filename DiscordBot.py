import datetime
from datetime import time
import asyncio
import discord
import pytz  # Import pytz

from WebScrapper import WebScrapper
from Parser import Parser

web_scrapper = WebScrapper("https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt")
parser = Parser(web_scrapper.get_lines())


class MyDiscordBot:
    def __init__(self, bot_token):
        # im thinking about doing instance based instances lmaooooooooo
        self.bot_token = bot_token
        self.bot = None
        self.tasks = {}

    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith('$uptime'):
            guild_id = message.guild.id
            guild = self.bot.get_guild(guild_id)
            channel = discord.utils.get(guild.channels, name='aurora-alert')
            await channel.send("I'm still working don't worry!")

        if message.guild:
            guild_id = message.guild.id
            if guild_id not in self.tasks:
                self.tasks[guild_id] = asyncio.create_task(self.scheduled_pin(guild_id))

    async def scheduled_pin(self, guild_id):
        # Retrieve guild-specific information here
        guild = self.bot.get_guild(guild_id)
        channel = discord.utils.get(guild.channels, name='aurora-alert')
        role = discord.utils.get(guild.roles, name="Aurora Alerts")
        msg = f"<@&{role.id}> \n Go see the northern lights on ``{parser.get_date_time_KP()[0][0]}`` at ``{parser.get_date_time_KP()[0][1]}``"

        next_target_datetime = None
        message_sent_today = False
        while True:
            # Use EST timezone for 'now'
            est_timezone = pytz.timezone("US/Eastern")
            now = datetime.datetime.now(est_timezone)
            target_time = time(7, 00)  # 5:35 PM (You can customize this per guild if needed)
            target_datetime = now.replace(hour=target_time.hour, minute=target_time.minute)

            if now >= target_datetime and not message_sent_today:
                if channel:
                    embedVar = discord.Embed(title="Aurora Alert", description=msg, color=0x00CCFF)
                    # select random url in a list and then set the image to that one
                    embedVar.set_image(
                        url="https://www.mtu.edu/tour/copper-country/northern-lights/images/northern-lights-michigan-tech-1600feature.jpg")
                    await channel.send(embed=embedVar)
                    print(f"Sending Alert to {guild.name}")
                    message_sent_today = True
                next_target_datetime = target_datetime + datetime.timedelta(days=1)

            elif now < target_datetime:
                if next_target_datetime is None:
                    next_target_datetime = target_datetime

                sleep_duration = 30.0
                await asyncio.sleep(sleep_duration)
                continue

            if message_sent_today:
                sleep_duration = (next_target_datetime - now).total_seconds()
                await asyncio.sleep(sleep_duration)

            if now.date() != next_target_datetime.date():
                print(f"New message is able to be sent in  {guild.name}")
                message_sent_today = False

    def run(self):
        intents = discord.Intents.all()
        intents.message_content = True  # Make sure this is enabled for on_message to work
        self.bot = discord.Client(intents=intents)
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)

        # Run the bot with your bot token
        self.bot.run(self.bot_token)
