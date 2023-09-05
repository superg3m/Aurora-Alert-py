from DiscordBot import MyDiscordBot

if __name__ == "__main__":
    bot_token = 'MTE0ODI4NzcxMjM5OTQ3ODkxNQ.G432we.zxH2NSi9mF9NWWjNbhHHANMR1vonwvDEm_PWDQ'

    # Create an instance of the ScheduledMessageBot class and run it
    bot = MyDiscordBot(bot_token)
    bot.run()