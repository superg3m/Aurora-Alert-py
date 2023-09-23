import ephem
import pytz
from datetime import datetime

# Set your local time zone here (e.g., 'America/New_York' for Eastern Time)
local_timezone = pytz.timezone('America/Detroit')

# Create a datetime object for the current date and time in your local time zone
current_datetime = datetime.now(local_timezone)
print(current_datetime)

# Create an observer for the moon
moon = ephem.Moon()

# Set the date to your local current date and time
moon.compute(current_datetime)

# Calculate the percentage of illumination (0.0 to 1.0)
illumination = moon.phase / 100

# IDK this isn't working

# Define moon phase names and their corresponding ranges of illumination
moon_phase_names = [
    ("New Moon", (0.0, 0.03)),
    ("Waxing Crescent", (0.03, 0.5)),
    ("First Quarter", (0.5, 0.53)),
    ("Waxing Gibbous", (0.53, 0.97)),
    ("Full Moon", (0.97, 1.0)),
    ("Waning Gibbous", (0.97, 0.53)),
    ("Last Quarter", (0.53, 0.5)),
    ("Waning Crescent", (0.5, 0.03)),
]

# Determine the moon phase based on the moon's age and percentage of illumination
moon_phase_name = None
for phase, (start, end) in moon_phase_names:
    if start <= illumination <= end:
        moon_phase_name = phase
        break

# Print the moon phase name
print(f"Current Moon Phase: {moon_phase_name}")
