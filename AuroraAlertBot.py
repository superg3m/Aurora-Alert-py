from enum import Enum
import datetime
from datetime import time
import asyncio
import discord
import pytz
import random

from WebScrapper import WebScrapper
from Parser import Parser

URLS = [
    "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
    "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
    "https://www.mtu.edu/tour/copper-country/northern-lights/images/northern-lights-michigan-tech-1600feature.jpg"
]

RESPONSE_NUMBER = 0

class STATUS(Enum):
    Idle_Status = -1
    Three_Day_Ping = 0
    Two_Day_Ping_With_Range = 1
    Day_Of_Ping = 2


class DATE(Enum):
    Day_One = 0
    Day_Two = 1
    Day_Three = 2


# Guild_ID: {"channel_name": "general",
#              "target_time": time(16, 30)},
#
#
#
url_scrap = "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt"
web_scrapper = WebScrapper(url_scrap)
parser = Parser(web_scrapper.get_lines())


class AuroraAlert:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.bot = None
        self.guild_settings = {

            # Add more guild settings here
        }

    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

        for guild in self.bot.guilds:
            if guild.id not in self.guild_settings:
                self.init_guild_settings(guild)

    def init_guild_settings(self, guild):
        role = discord.utils.get(guild.roles, name="Aurora Alerts")
        channel = discord.utils.get(guild.channels, name='aurora-alert')
        print(f"Init: {guild.name} | ID: {guild.id}")
        self.guild_settings[guild.id] = {
            'message_sent': False,
            'sleep_duration': 0,
            'schedule_loop': asyncio.create_task(self.check_scheduled_tasks(guild.id)),
            'channel_name': 'aurora-alert',
            'target_time': time(7, 00),
            'role_instance': role,
            'channel_instance': channel,
            'guild_instance': guild
        }

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Check if the message is from a specific guild by comparing guild ID
        global RESPONSE_NUMBER
        if RESPONSE_NUMBER == 0:
            if message.content.startswith('$uptime'):
                RESPONSE_NUMBER += 1
                await message.channel.send("I'm still working don't worry!")
                RESPONSE_NUMBER -= 1

            if message.content.startswith('$target_time'):
                RESPONSE_NUMBER += 1
                await self.target_time_command(message)
                RESPONSE_NUMBER -= 1

            if message.content.startswith('$channel_name'):
                RESPONSE_NUMBER += 1
                await self.channel_name_command(message)
                RESPONSE_NUMBER -= 1

    async def uptime_command(self, message):
        """

        :param message:
        :return:
        """

    async def target_time_command(self, message):
        guild_id = message.guild.id
        channel = self.guild_settings[guild_id]['channel_instance']
        await channel.send('Remember this is a 24 hour clock ex: time(16, 30) is 4:30pm')

        tempSTR = message.content.replace('$target_time', '')
        tempSTR = tempSTR.replace('time(', '')
        tempSTR = tempSTR.replace(')', '')
        tempSTR = tempSTR.split(', ')

        self.guild_settings[guild_id]['target_time'] = time(int(tempSTR[0]), int(tempSTR[1]))
        await channel.send('Successfully updated the target time!')

    async def channel_name_command(self, message):
        guild_id = message.guild.id
        channel = self.guild_settings[guild_id]['channel_name']
        await channel.send('Default is aurora-alert')

        tempSTR = message.content.replace('$channel_name ')

        self.guild_settings[guild_id]['channel_name'] = time(int(tempSTR[0]), int(tempSTR[1]))
        await channel.send('Successfully updated the channel name!')

    async def send_message_to_guild(self, guild_id, message):
        settings = self.guild_settings.get(guild_id)
        guild = settings['guild_instance']
        role = settings['role_instance']
        if guild and await self.message_timer(settings) and len(parser.get_date_time_KP()) > 0:
            msg = f"<@&{role.id}> \n Go see the northern lights on \n"

            for my_tuple in parser.get_date_time_KP():
                my_date, my_time, my_kp = my_tuple
                msg += f"``{my_date}`` at ``{my_time}`` | ``kp index: {my_kp}`` \n"

            channel = settings['channel_instance']
            embedVar = discord.Embed(title="Aurora Alert", description=msg, color=0x00CCFF)
            embedVar.set_image(
                url=random.choice(URLS))

            settings['message_sent'] = True
            await channel.send(embed=embedVar)
            print(f"Sending Alert to {guild.name}")

    def trigger_timer(self, settings):
        # Use EST timezone for 'now'
        est_timezone = pytz.timezone("US/Eastern")
        now = datetime.datetime.now(est_timezone)
        target_time = settings['target_time']
        target_datetime = now.replace(hour=target_time.hour, minute=target_time.minute)
        next_target_datetime = target_datetime + datetime.timedelta(days=1)
        sleep_duration = (next_target_datetime - now).total_seconds()
        settings['sleep_duration'] = sleep_duration
        if now < target_datetime:
            return False

        return True

    async def message_timer(self, settings):

        while self.trigger_timer(settings) is False:
            await asyncio.sleep(30)

        if settings['message_sent'] is True:
            await asyncio.sleep(settings['sleep_duration'])
            settings['message_sent'] = False
            web_scrapper.re_scrap(url_scrap)
            parser.re_parse(web_scrapper.get_lines())
            print(f"new data is here!")

        return True

    async def check_scheduled_tasks(self, guild_id):
        while True:
            # and guild_id != 1141878631002546231 and guild_id != 1147262863921135768
            if guild_id in self.guild_settings and guild_id != 1141878631002546231 and guild_id != 1147262863921135768:
                await self.send_message_to_guild(guild_id, "Your scheduled message here")
            await asyncio.sleep(30)  # Check every minute

    def start_bot(self):
        intents = discord.Intents.all()
        intents.message_content = True  # Make sure this is enabled for on_message to work
        self.bot = discord.Client(intents=intents)

        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)

        self.bot.run(self.bot_token)
