import pytz
import requests
import datetime


class CloudCoverage:
    def __init__(self):
        # Replace with your OpenWeatherMap API key
        self.api_key = "391c28fa1bffe5bac10ae9e07d85f9e7"
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        self.city = "Houghton, US"

    def get_cloud_coverage(self):
        url = f"{self.base_url}q={self.city}&appid={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"cloud coverage {data['clouds']['all']}%")
            return data['clouds']['all']
        else:
            print("Erorr when fetching the weather data")

    def get_cloud_coverage_for_next_3_days(self):
        # Specify the latitude and longitude for Houghton, UP, Michigan
        latitude = 47.1211
        longitude = -88.5694

        # Calculate timestamps for the next 3 days at 19:00 EST
        time_zone = pytz.timezone("US/Eastern")
        today = datetime.datetime.now(time_zone)
        next_three_days = [today + datetime.timedelta(days=i) for i in range(3)]

        cloud_coverages = {}

        for day in next_three_days:
            # Determine the date of the current day
            current_date = day.strftime('%Y-%m-%d')

            TIME_ZONE = pytz.timezone('US/Eastern')
            current_time_est = datetime.datetime.now(TIME_ZONE)
            is_dst = current_time_est.dst()
            time_zone_offset = 3600 * -(4 + int(is_dst.seconds / 3600))

            # Build the API request URL with the specified date and time
            url = f"{self.base_url}lat={latitude}&lon={longitude}&appid={self.api_key}&timezone={time_zone_offset}"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                # Extract cloud cover information (in percentage)
                cloud_coverage = data['list']
                print(f"Cloud cover in Houghton, MI on {current_date} at 19:00 EST: {cloud_coverage}%")

                formatted_date = day.strftime('%b %d')
                cloud_coverages[formatted_date] = f"{cloud_coverage}%"

            else:
                print(f"Error fetching weather data for {current_date}")

        # Return the nighttime cloud coverages
        return cloud_coverages


if __name__ == "__main__":
    cloud = CloudCoverage()
    print(cloud.get_cloud_coverage_for_next_3_days())
