import json
import os

import requests
from enum import Enum
from ServerLogger import logger
from dotenv import load_dotenv

class MoonCycle(Enum):
    NEW_MOON = 1
    QUARTER_MOON = 2
    HALF_MOON = 3
    THREE_QUARTER_MOON = 4
    FULL_MOON = 5

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPEN_WEATHER_API")
        self.city = "Houghton, US"

    def get_visibility_percentage(self) -> int:
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        url = f"{base_url}?q={self.city}&appid={self.api_key}&units=imperial"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            json_str = json.dumps(data, indent=4)
            print(json_str)

            max_visibility_in_meters = 10_000

            return data["visibility"] / max_visibility_in_meters
        else:
            logger.error("Error when fetching the weather data")

if __name__ == "__main__":
    load_dotenv()
    cloud = WeatherAPI()
    print(cloud.get_visibility_percentage())
