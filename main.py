import os

from dotenv import load_dotenv
# from AuroraAlertBot import AuroraAlert
import sqlite3
import time

from Frontend.DiscordBot.AuroraAlertBot import AuroraAlert


def main():
    conn = sqlite3.connect('Backend/Database/AuroraAlert.db')

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    seconds_since_epoch = time.time()
    print(seconds_since_epoch)

    conn.close()

    bot = AuroraAlert(bot_token, conn)
    bot.start_bot()


if __name__ == "__main__":
    main()
