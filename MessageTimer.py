import asyncio
import datetime

import pytz


class MessageTimer:
    def __init__(self):
        self.message_event = asyncio.Event()
        self.running = False
        self.result = False

    def check_timer(self):
        # Set the Eastern Time Zone (EST)
        est_timezone = pytz.timezone('US/Eastern')

        # Get the current datetime in the EST time zone
        now = datetime.datetime.now(est_timezone)

        # Adjust the target time to EST (change to your target time)
        target_time = est_timezone.localize(
            datetime.datetime(now.year, now.month, now.day, 12, 0))  # Adjust to your target time

        # Check if it's time to send a message
        return now >= target_time

    async def reset_timer(self):
        # Implement your logic to reset the timer conditions
        print("Resetting timer")
        await asyncio.sleep(86400)  # Sleep for a day (86400 seconds)
        self.result = False
        self.message_event.clear()

    async def start(self):
        if self.running:
            return
        self.running = True

        while self.running:
            if self.check_timer():
                if not self.message_event.is_set():
                    self.message_event.set()
                    self.result = True  # Set the result to True when it's time to send
                    await self.reset_timer()  # Reset the timer after sending

    def stop(self):
        self.running = False
        self.message_event.set()  # Ensure it exits wait() if waiting

    def make_result_false(self):
        self.result = False

    def get_result(self):
        return self.result
