# https://github.com/python-pillow/Pillow/discussions/6927

import os
import sys
import io

from PIL import Image
from PIL import ImageOps
from PIL import TiffImagePlugin

img_path = sys.argv[1]

src_img = Image.open(img_path)
exif = src_img.getexif()

# del exif[TiffImagePlugin.STRIPOFFSETS]

for key, value in exif.items():
    if isinstance(value, tuple):
        print(key)
        del exif[key]

dst_img = ImageOps.exif_transpose(src_img).convert("RGB")

output_file = io.BytesIO()
dst_img.save(output_file, "jpeg", quality=95, exif=exif)