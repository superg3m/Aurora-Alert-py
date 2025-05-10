import asyncio

import discord
from discord.ext.commands import bot

from Backend.Models.Guild import GuildConfig

blacklisted_guild_ids = [1141878631002546231, 1147262863921135768]

class AuroraAlert:
    def __init__(self, db_connection):
        self.bot = None
        self.db_connection = db_connection
        self.guild_configurations: dict[int, GuildConfig] = {}
        self.guild_conditions: dict[int, asyncio.Condition] = {}
        self.guild_tasks: dict[int, asyncio.Task] = {}


    # TODO(Jovanni): rethink this?
    async def guild_coroutine_should_send_message(self, guild_id) -> bool:
        seconds_to_sleep = 0
        while True:



            if time_to_send_message:
                return True

            await asyncio.sleep(seconds_to_sleep)

    async def guild_coroutine(self, guild_id):


        condition: asyncio.Condition = self.guild_conditions[guild_id]
        while True:
            await condition.acquire()
            try:
                # check for db updates
                # re-get all api data
                await condition.wait_for(self.guild_coroutine_should_send_message(guild_id))
                # check if message should send
            finally:
                condition.release()

    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

        self.guild_configurations = GuildConfig.load_all(self.db_connection)

        for guild in self.bot.guilds:
            if guild.id in blacklisted_guild_ids:
                continue

            self.init_guild(guild)

    async def on_guild_join(self, guild):
        print(f"Bot joined a new guild: {guild.name} (ID: {guild.id})")
        self.init_guild(guild)

    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if before.name != after.name:
            guild_config = self.guild_configurations[before.id]
            guild_config.name = after.name
            guild_config.update(self.db_connection)

    async def on_guild_remove(self, guild):
        self.guild_conditions.pop(guild.id)
        self.guild_tasks.pop(guild.id).cancel()

    def init_guild(self, guild):
        self.guild_conditions[guild.id] = asyncio.Condition()

        # NOTE(Jovanni): If the sqlite database has config settings for this guild id just use those
        if guild.id not in self.guild_configurations:
            self.guild_configurations[guild.id] = GuildConfig(guild.id, guild.name)

        self.guild_tasks[guild.id] = asyncio.create_task(self.guild_coroutine(guild.id))



    def start_bot(self, bot_token):
        intents = discord.Intents.all()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        self.bot = discord.Client(intents=intents)

        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.event(self.on_guild_join)
        self.bot.event(self.on_guild_update)
        self.bot.event(self.on_guild_remove)

        self.bot.run(bot_token)

