import os

from dotenv import load_dotenv
import sqlite3
import time

from ServerLogger import logger

def main():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    conn = sqlite3.connect('old/Backend/Database/AuroraAlert.db')

    bot = AuroraAlert(conn)
    bot.start_bot(bot_token)
    conn.close()

if __name__ == "__main__":
    logger.info(f"Aurora Alert Online!")
    main()
    logger.info(f"Aurora Alert Down!")
