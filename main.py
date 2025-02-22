import os

from dotenv import load_dotenv
# from AuroraAlertBot import AuroraAlert
import sqlite3


def main():
    conn = sqlite3.connect('./Database/guild.db')
    cursor = conn.cursor()

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    conn.close()

    return
    # bot = AuroraAlert(bot_token)
    #bot.start_bot()


if __name__ == "__main__":
    main()
