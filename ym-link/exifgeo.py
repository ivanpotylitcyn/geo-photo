from exif import Image
import sys

img_path = sys.argv[1]

def convert(deg, min, sec, ref):
    return (float(deg) + float(min) / 60 + float(sec) / (60 * 60)) * (-1 if ref in ['W', 'S'] else 1)

with open(img_path, 'rb') as src:
    img = Image(src)

if img.has_exif:
    info = f" has the EXIF {img.exif_version}"
else:
    info = "does not contain any EXIF information"
    sys.exit()

print(f"Image {src.name}: {info}")

lat = img.gps_latitude
lon = img.gps_longitude

geoLat = f"{int(lat[0])}°{int(lat[1])}\'{lat[1] % 1 * 60:.1f}\"{img.gps_latitude_ref}"
geoLon = f"{int(lon[0])}°{int(lon[1])}\'{lon[1] % 1 * 60:.1f}\"{img.gps_longitude_ref}"

latDd = convert(lat[0], lat[1], lat[2], img.gps_latitude_ref)
lonDd = convert(lon[0], lon[1], lon[2], img.gps_longitude_ref)

link = f"https://yandex.ru/maps/?pt={lonDd},{latDd}&z=18&l=map"

print()
print(geoLat, geoLon)
print(img.datetime_original.replace(':', '-', 2))
print()
print(link)