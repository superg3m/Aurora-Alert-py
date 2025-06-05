import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.created_time = datetime.fromtimestamp(record.created).strftime("%I:%M%p").lower().lstrip("0")
        return f"{record.created_time} | {record.levelname}: {record.getMessage()}"

def init_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    current_date = datetime.now().strftime("%m.%d.%y")
    log_filename = f"logs/{current_date}.log"


    l = logging.getLogger()
    l.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(
        filename=log_filename,  # Use date as filename in logs directory
        when="midnight",        # Rotate at midnight
        interval=1,             # Rotate every day
        backupCount=7,          # Keep 7 days of logs (1 week)
    )

    handler.suffix = "%m.%d.%y"
    formatter = CustomFormatter()
    handler.setFormatter(formatter)
    l.addHandler(handler)

    return l

logger = init_logger()