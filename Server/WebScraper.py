import asyncio
import requests


class WebScraper:
    def __init__(self, url):
        self.__url = url
        self.__response = requests.get(self.__url)
        self.__lines = self.__response.text.splitlines()

    def re_scrap(self, url):
        self.__url = url
        self.__response = requests.get(self.__url)
        self.__lines = self.__response.text.splitlines()

    def get_lines(self):
        return self.__lines

    def get_url(self):
        return self.__url
