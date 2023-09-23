from enum import Enum
from datetime import time
import asyncio
import discord
import random
import threading

from CloudCoverage import CloudCoverage
from WebScraper import WebScraper
from MessageTimer import MessageTimer

from Parser import Parser

URLS = [
    "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?ixlib=rb-4.0.3&ixid"
    "=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",

    "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?ixlib=rb-4.0.3&ixid"
    "=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",

    "https://www.mtu.edu/tour/copper-country/northern-lights/images/northern-lights-michigan-tech-1600feature.jpg"
]

Reading_Message_Thread = False
ACTIVE_WEB_SCRAP_INSTANCE = False


class STATUS(Enum):
    Idle_Status = -1
    Three_Day_Ping = 0
    Two_Day_Ping_With_Range = 1
    Day_Of_Ping = 2


class DATE(Enum):
    Day_One = 0
    Day_Two = 1
    Day_Three = 2


url_scrap = "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt"

cloud_coverage = CloudCoverage()
web_scraper = WebScraper(url_scrap)
message_timer = MessageTimer()

blacklisted_guilds = [1141878631002546231, 1147262863921135768]


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
            'message_queued': False,
            'schedule_loop': asyncio.create_task(self.check_scheduled_tasks(guild.id)),
            'channel_name': 'aurora-alert',
            'target_time': time(13, 0),
            'role_instance': role,
            'channel_instance': channel,
            'guild_instance': guild,
            'kp_index_threshold': 4.67,
            'cloud_coverage_threshold': 35,
            'parser_instance': None,
        }
        settings = self.guild_settings.get(guild.id)
        settings['parser_instance'] = Parser(settings.get('kp_index_threshold'), web_scraper.get_lines())

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Check if the message is from a specific guild by comparing guild ID
        global Reading_Message_Thread

        if not Reading_Message_Thread:
            if message.content.startswith('$uptime'):
                Reading_Message_Thread = True
                await self.uptime_command(message)

            if message.content.startswith('$target_time'):
                Reading_Message_Thread = True
                # await self.target_time_command(message)
                # TODO: Implement this

            if message.content.startswith('$channel_name'):
                Reading_Message_Thread = True
                # await self.channel_name_command(message)
                # TODO: Implement this

            Reading_Message_Thread = False

    async def uptime_command(self, message):
        await message.channel.send("I'm still working don't worry!")

    async def target_time_command(self, message):
        guild_id = message.guild.id
        settings = self.guild_settings.get(guild_id)
        channel = settings.get('channel_instance')
        await channel.send('Remember this is a 24 hour clock ex: time(16, 30) is 4:30pm')

        tempSTR = message.content.replace('$target_time', '')
        tempSTR = tempSTR.replace('time(', '')
        tempSTR = tempSTR.replace(')', '')
        tempSTR = tempSTR.split(', ')

        settings['target_time'] = time(int(tempSTR[0]), int(tempSTR[1]))
        await channel.send('Successfully updated the target time!')

    async def channel_name_command(self, message):
        guild_id = message.guild.id
        settings = self.guild_settings.get(guild_id)
        channel = settings.get('channel_name')
        await channel.send('Default is aurora-alert')

        tempSTR = message.content.replace('$channel_name ')

        settings['channel_name'] = time(int(tempSTR[0]), int(tempSTR[1]))
        await channel.send('Successfully updated the channel name!')

    async def send_message_to_guild(self, guild_id):
        settings = self.guild_settings.get(guild_id)
        guild_instance = settings.get('guild_instance')
        role_instance = settings.get('role_instance')
        parser_instance = settings.get('parser_instance')
        kp_list_length = len(parser_instance.get_date_time_KP())
        # and cloud_coverage.get_cloud_coverage() <= settings.get('cloud_coverage_threshold']
        if (
              guild_instance and settings.get('message_queued') and kp_list_length > 0
        ):
            msg = f"<@&{role_instance.id}> \n Go see the northern lights on \n"

            for my_tuple in settings.get('parser_instance').get_date_time_KP():
                my_date, my_time, my_kp = my_tuple
                msg += f"``{my_date}`` at ``{my_time}``, ``kp-index: {my_kp}`` \n"

            channel = settings.get('channel_instance')
            embedVar = discord.Embed(title="Aurora Alert", description=msg, color=0x00CCFF)
            embedVar.set_image(
                url=random.choice(URLS))

            settings['message_sent'] = True
            settings['message_queued'] = False

            await channel.send(embed=embedVar)
            print(f"Sending Alert to {guild_instance.name}")

    async def check_scheduled_tasks(self, guild_id):
        timer = 0
        reparse_interval = 86400  # 24 hours in seconds\
        settings = self.guild_settings.get(guild_id)

        while True:
            if guild_id in self.guild_settings:
                if not settings.get('message_sent'):
                    settings['message_queued'] = message_timer.get_result()

                await self.send_message_to_guild(guild_id)

            if timer >= reparse_interval:
                # Restart the timer
                timer = 0
                kp_threshold_index = settings.get('kp_index_threshold')
                web_scraper.re_scrap(url_scrap)
                settings['parser_instance'].re_parse(kp_threshold_index, web_scraper.get_lines())
                settings['message_sent'] = False
            await asyncio.sleep(30)  # Check every minute
            timer += 30  # Increment timer by 30 seconds

    def start_timers(self):
        def message_thread_timer():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Start the event loop for WebScraper
            asyncio.run(message_timer.start())

        message_thread = threading.Thread(target=message_thread_timer)
        message_thread.start()

    def start_bot(self):
        intents = discord.Intents.all()
        intents.message_content = True  # Make sure this is enabled for on_message to work
        self.start_timers()

        self.bot = discord.Client(intents=intents)

        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)

        self.bot.run(self.bot_token)
