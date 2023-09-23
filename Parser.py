import re

from colorama import Fore
from TimeConverter import TimeConverter

time_converter = TimeConverter()
lookup_keys = ["00-03UT", "03-06UT", "06-09UT", "09-12UT", "12-15UT", "15-18UT", "18-21UT", "21-00UT"]
utc_hours = [0, 3, 6, 9, 12, 15, 18, 21]


# fix the time
def remove_inside_and_parentheses(input_string):
    # Define a regular expression pattern to match text within parentheses and the parentheses themselves
    pattern = r'\([^)]*\)'

    # Use re.sub to replace matched patterns with an empty string
    result = re.sub(pattern, '', input_string)

    return result


class Parser:
    def __init__(self, kp_index_threshold, lines):
        self.__lines = lines
        self.__data_range = []
        self.__date_time_KP = []

        self.__parse_dates()

        self.__kp_index_threshold = kp_index_threshold

        self.__report = {
            "dates": [self.__data_range[0], self.__data_range[1], self.__data_range[2]],
            "KP": [[], [], []]
        }

        self.__parse_report()
        self.__calculate_report()

    def re_parse(self, kp_thresh_hold, lines):
        self.__lines = lines
        self.__data_range = []
        self.__date_time_KP = []

        self.__parse_dates()

        self.__kp_index_threshold = kp_thresh_hold

        self.__report = {
            "dates": [self.__data_range[0], self.__data_range[1], self.__data_range[2]],
            "KP": [[], [], []]
        }

        self.__parse_report()
        self.__calculate_report()

    def find_best_time_per_day(self):
        best = {self.__data_range[0]: [],
                self.__data_range[1]: [],
                self.__data_range[2]: []}

        for arr in self.__date_time_KP:
            date, time, KP = arr
            print(arr)
            best.get(date).append(KP)

    def __calculate_report(self):
        for i, KPArr in enumerate(self.__report.get('KP')):
            for j, KP in enumerate(KPArr):
                est_24_hour = TimeConverter.utc_to_est_24(utc_hours[j])
                if float(KP) >= self.__kp_index_threshold and est_24_hour >= 7 and est_24_hour >= 19:
                    # print(f"24 hour: {est_24_hour}")
                    #self.__date_time_KP[self.__report.get('dates')[i]] = (
                     #   (self.__report.get('dates')[i], time_converter.get_est_format(utc_hours[j]), float(KP)))

                    self.__date_time_KP.append((self.__report.get('dates')[i], time_converter.get_est_format(utc_hours[j]), float(KP)))

                    # print(f"Report# {j + 1} | Date: {self.__report.get('dates')[i]} | {Fore.RED}KP: {KP}{
                    # Fore.RESET} | {time_converter.get_est_format(utc_hours[j])}")
                else:
                    """
                    Yes
                    """
                    # print(f"Report# {j + 1} | Date: {self.__report.get('dates')[i]} | KP: {KP} | {time_converter.get_est(utc_hours[j])}")
            # print()

    def get_date_ranges(self):
        return self.__data_range

    def get_date_time_KP(self):
        return self.__date_time_KP

    def get_pings(self):
        # print(f"Date: {self.__report.get('dates')[i]} | {Fore.RED}KP: {KP}{Fore.RESET} | {time_converter.get_est(utc_hours[j])}")
        return ""

    def __parse_dates(self):
        search_phrase = "NOAA Kp index forecast"

        temp_str = ""
        for i in range(len(self.__lines) - 1):
            current_line = self.__lines[i]
            if search_phrase in current_line:
                temp_str = self.__lines[i + 1].replace(" ", '')

        self.__calculate_date_range(temp_str)

    def __parse_report(self):
        for line in self.__lines:
            for i in range(len(lookup_keys)):
                if lookup_keys[i] in line:
                    line = line.replace(lookup_keys[i], "")
                    line = remove_inside_and_parentheses(line)
                    line = " ".join(line.split())
                    indexes = line.split(" ")
                    self.__report.get("KP")[0].append(indexes[0])
                    self.__report.get("KP")[1].append(indexes[1])
                    self.__report.get("KP")[2].append(indexes[2])

    def __calculate_date_range(self, temp_str):
        string_builder = ""
        number_count = 0
        for char in temp_str:
            if char.isdigit():
                number_count += 1

                if number_count == 1:
                    string_builder += " "

                string_builder += char
            else:
                string_builder += char

            if number_count == 2:
                self.__data_range.append(string_builder)
                string_builder = ""
                number_count = 0
