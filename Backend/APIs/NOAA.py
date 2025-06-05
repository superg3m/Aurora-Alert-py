import re

from Backend import Utils


class NOAA_DayData:
    def __init__(self, day: int, month: str, kp_indices: list[float]):
        self.day: int = day
        self.month: str = month
        self.kp_indices: list[float] = kp_indices

    def __repr__(self):
        return f"{self.month} | {self.day} | {self.kp_indices}"


def noaa_parse() -> list[NOAA_DayData]:
    scraped_lines: list[str] = Utils.scrape("https://services.swpc.noaa.gov/text/3-day-forecast.txt")

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

    ret = []
    for i in range(len(kp)):
        month_day = three_dates[i].split(" ")

        ret.append(
            NOAA_DayData(
                int(month_day[1]),
                month_day[0],
                kp[three_dates[i]])
        )

    print(ret)

    return ret


if __name__ == "__main__":
    noaa_data = noaa_parse()
    pass
