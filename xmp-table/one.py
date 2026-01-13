import os
import argparse
import json

from libxmp import XMPFiles, consts
from libxmp.utils import file_to_dict

def dump_xmp_to_json(photo_filename, out_filename):
    dict = file_to_dict(file_path=photo_filename)
    with open(out_filename, 'w', encoding='utf-8') as file:
        json.dump(dict, file, indent=4, ensure_ascii=False)

def get_xmp_metadata(photo_filename):
    print(f"Обабатывается файл: {photo_filename}")
    dict = file_to_dict(file_path=photo_filename)

    metadata = {}

    dc = dict["http://purl.org/dc/elements/1.1/"]
    for element in dc:
        keys = ['title', 'creator', 'description', 'rights', 'publisher', 'identifier']
        for key in keys:
            if key in element[0] and element[1] != '' and 'x-default' not in element[1]:
                print(f"{element[0]}: {element[1]}")
                metadata[key] = element[1]

    exif = dict["http://ns.adobe.com/exif/1.0/"]
    for element in exif:
        keys = ['Longitude', 'Latitude', 'DateTimeOriginal']
        for key in keys:
            if key in element[0] and element[1] != '':
                print(f"{element[0]}: {element[1]}")
                metadata[key] = element[1]

    print(json.dumps(metadata, indent=4, ensure_ascii=False))
    print()
    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Извлечение EXIF данных из фотографий')
    parser.add_argument('image', help='Путь к фотографии')
    
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Ошибка: Файл '{args.image}' не существует")
        exit(1)
    
    dump_xmp_to_json(args.image, 'out.json')
    get_xmp_metadata(args.image)