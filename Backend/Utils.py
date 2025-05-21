import time
import requests
from datetime import datetime

us_time_zone_offsets = {
    "UTC": 0,
    "EST": -5,  # Eastern Standard Time
    "EDT": -4,  # Eastern Daylight Time
}

def scrape(url) -> list[str]:
    response = requests.get(url)
    return response.text.splitlines()

def utc_to_other_time_zone(time_zone: str, utc_time: int) -> int:
    HOUR_OFFSET = us_time_zone_offsets[time_zone]
    if time.daylight:
        HOUR_OFFSET += 1

    if utc_time + HOUR_OFFSET <= 0:
        return 24 - ((utc_time + HOUR_OFFSET) % 24)
    else:
        return (utc_time + HOUR_OFFSET) % 24

def format_24hr_to_12hr(_24_hr_time) -> str:
    if _24_hr_time == 0:
        return f"12:00am"
    elif _24_hr_time < 12:
        return f"{_24_hr_time}:00am"
    else:
        return f"{_24_hr_time - 12}:00pm"


seconds_epsilon = 120
def days_to_seconds(days):
    return days * 86400
