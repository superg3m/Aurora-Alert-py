class TimeConverter:
    @staticmethod
    def utc_to_est_12hr_am_pm(utc_hour):
        # Convert UTC hour to EST hour
        est_hour = (utc_hour - 5)
        am_pm = "AM"

        if est_hour < 0:
            est_hour = est_hour + 12
            am_pm = "PM"

        # Determine AM or PM
        if est_hour >= 12:
            est_hour = est_hour - 12
            am_pm = "PM"
        if est_hour == 0:
            est_hour = 12

        # Return formatted time
        return f"{est_hour:02d}:00 {am_pm}"

    def get_est_format(self, n):
        est_time = TimeConverter.utc_to_est_12hr_am_pm(n)
        return est_time

    def get_est(self, n):
        est_time = TimeConverter.utc_to_est_24(n)
        return est_time

    @staticmethod
    def utc_to_est_24(utc_hour):
        # Convert UTC hour to EST hour
        est_hour = (utc_hour - 5) % 24  # Subtract 4 hours to convert to EST and wrap around to 0-23

        # Special case for midnight
        if est_hour == 0:
            est_hour = 12

        # Return formatted time
        return est_hour
