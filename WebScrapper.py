import requests
from colorama import Fore
from TimeConverter import TimeConverter

time_converter = TimeConverter()
lookup_keys = ["00-03UT", "03-06UT", "06-09UT", "09-12UT", "12-15UT", "15-18UT", "18-21UT", "21-00UT"]


class WebScrapper:
    def __init__(self, url):
        self.__url = url

        self.__response = requests.get(self.__url)

        self.__lines = self.__response.text.splitlines()

    def get_lines(self):
        return self.__lines

    def get_url(self):
        return self.__url
