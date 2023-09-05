class TimeConverter:
    @staticmethod
    def utc_to_est_12hr_am_pm(utc_hour):
        # Convert UTC hour to EST hour
        est_hour = (utc_hour - 4) % 12

        # Determine AM or PM
        am_pm = "AM" if utc_hour < 12 else "PM"

        # Special case for midnight
        if est_hour == 0:
            est_hour = 12

        # Return formatted time
        return f"{est_hour:02d}:00 {am_pm}"

    def get_est(self, n):

        est_time = TimeConverter.utc_to_est_12hr_am_pm(n)
        return est_time + (" (EST)")
