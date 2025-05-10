import os

from dotenv import load_dotenv
import sqlite3
import time

from old.Frontend.DiscordBot.AuroraAlertBot import AuroraAlert


def main():
    conn = sqlite3.connect('old/Backend/Database/AuroraAlert.db')

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    seconds_since_epoch = time.time()
    print(seconds_since_epoch)

    conn.close()

    bot = AuroraAlert(conn)
    bot.start_bot(bot_token)


if __name__ == "__main__":
    main()
