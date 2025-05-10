import ephem
import pytz
from datetime import datetime

local_timezone = pytz.timezone('America/Detroit')
current_datetime = datetime.now(local_timezone)
print(current_datetime)
moon = ephem.Moon()
moon.compute(current_datetime)
illumination = moon.phase / 100

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

moon_phase_name = None
for phase, (start, end) in moon_phase_names:
    if start <= illumination <= end:
        moon_phase_name = phase
        break

print(f"Current Moon Phase: {moon_phase_name}")