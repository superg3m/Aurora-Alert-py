import discord

from Backend.Models.Guild import Guild

blacklisted_guilds = [1141878631002546231, 1147262863921135768]

class AuroraAlert:
    def __init__(self, db_conn):
        self.bot = None
        self.db_conn = db_conn
        self.guilds: list[Guild]

    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

        self.guilds = Guild.get_all_guild_data(self.db_conn)

        for guild in self.bot.guilds:
            if guilds.id in blacklisted_guilds:
                continue

    def init_guild(self, guild_id):
        self.server_conditions[guild_id] = asyncio.Condition()
        self.server_settings[guild_id] = None  # Initial setting
        self.server_tasks[guild_id] = asyncio.create_task(self.server_worker(guild_id))

    def start_bot(self, bot_token):
        intents = discord.Intents.all()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        self.bot = discord.Client(intents=intents)

        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.event(self.on_member_join)

        self.bot.run(bot_token)

