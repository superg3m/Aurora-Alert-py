import time
from datetime import datetime

import pytz
import requests

us_time_zone_offsets = {
    "UTC": 0,
    "EST": -5,  # Eastern Standard Time
    "EDT": -4,  # Eastern Daylight Time
    "CST": -6,  # Central Standard Time
    "CDT": -5,  # Central Daylight Time
    "MST": -7,  # Mountain Standard Time
    "MDT": -6,  # Mountain Daylight Time
    "PST": -8,  # Pacific Standard Time
    "PDT": -7,  # Pacific Daylight Time
    "AKST": -9,  # Alaska Standard Time
    "AKDT": -8,  # Alaska Daylight Time
}


def scrap(url) -> list[str]:
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
