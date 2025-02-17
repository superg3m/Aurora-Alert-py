from dotenv import load_dotenv
from AuroraAlertBot import AuroraAlert
import asyncio
import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('guild.db')
    cursor = conn.cursor()

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    bot = AuroraAlert(bot_token)
    bot.start_bot()

    conn.close()
