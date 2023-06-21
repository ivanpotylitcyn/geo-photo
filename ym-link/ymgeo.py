import sys
import math

def convert(lat, lon):
    latFrac, latInt = math.modf(lat)
    latInt = int(latInt)
    latMin = int(math.floor(latFrac * 60))
    latSec = round(latFrac * 60 * 60 - latMin * 60, 1)
    latRef = 'N' if lat > 0 else 'S'

    lonFrac, lonInt = math.modf(lon)
    lonInt = int(lonInt)
    lonMin = int(math.floor(lonFrac * 60))
    lonSec = round(lonFrac * 60 * 60 - lonMin * 60, 1)
    lonRef = 'E' if lon > 0 else 'W'

    geoString = f"{latInt}°{latMin}\'{latSec}\"{latRef} {lonInt}°{lonMin}\'{lonSec}\"{lonRef}"

    return geoString

coordsFloat = sys.argv[1]
lat, lon = [float(x) for x in coordsFloat.split(", ")]

print()
print(convert(lat, lon))
print(f"https://yandex.ru/maps/?pt={lon},{lat}&z=18&l=map")
print()