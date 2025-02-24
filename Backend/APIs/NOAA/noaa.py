import re

from Backend import Utils


class NOAA_Data:
    def __init__(self, day: int, month: str, kp_index: float):
        self.day: int = day
        self.month: str = month
        self.kp_index: float = kp_index


def noaa_parse() -> NOAA_Data:
    scraped_lines: list[str] = Utils.scrap("https://services.swpc.noaa.gov/text/3-day-forecast.txt")

    SEARCH_PHRASE_START = "00-03UT"
    SEARCH_PHRASE_END = "21-00UT"
    SEARCH_PHRASE_START_INDEX = -1
    SEARCH_PHRASE_END_INDEX = -1

    for i in range(len(scraped_lines)):
        line = scraped_lines[i]
        if SEARCH_PHRASE_START in line:
            SEARCH_PHRASE_START_INDEX = i

        if SEARCH_PHRASE_END in line:
            SEARCH_PHRASE_END_INDEX = i
            break

    dates_index = SEARCH_PHRASE_START_INDEX - 1
    kp_index_start = dates_index + 1
    kp_index_end = SEARCH_PHRASE_END_INDEX

    kp_lines = scraped_lines[kp_index_start:kp_index_end + 1]
    three_dates = re.sub(r"\s+", " ", scraped_lines[dates_index]).strip().split(" ")
    three_dates = [
        three_dates[0] + " " + three_dates[1],
        three_dates[2] + " " + three_dates[3],
        three_dates[4] + " " + three_dates[5]
    ]

    kp = {
        three_dates[0]: [],
        three_dates[1]: [],
        three_dates[2]: []
    }
    for line in kp_lines:
        canonical_lines = re.sub(r"\s+", " ", line).strip().split(" ")

        kp[three_dates[0]].append(canonical_lines[1])
        kp[three_dates[1]].append(canonical_lines[2])
        kp[three_dates[2]].append(canonical_lines[3])

    print(kp)

    return NOAA_Data(3, "feb", 2)


if __name__ == "__main__":
    noaa_data = noaa_parse()
    pass
