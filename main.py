import os

from dotenv import load_dotenv
# from AuroraAlertBot import AuroraAlert
import sqlite3
import time

seconds_epsilon = 120


def days_to_seconds(days):
    return days * 86400


def main():
    conn = sqlite3.connect('Database/AuroraAlert.db')
    cursor = conn.cursor()

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    print(bot_token)

    seconds_since_epoch = time.time()
    print(seconds_since_epoch)

    conn.close()

    return
    # bot = AuroraAlert(bot_token)
    # bot.start_bot()


if __name__ == "__main__":
    main()
