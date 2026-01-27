import one

import argparse
import os
import json
import csv

def read_folder_xmp(folder_path):
    print(f"Сканирование папки: {folder_path}")

    data = []

    for filename in os.listdir(folder_path):
        file_ext = os.path.splitext(filename)[1].lower()

        if '.jpg' not in file_ext:
            continue

        file_path = os.path.join(folder_path, filename)
        
        file_metadata = one.get_xmp_metadata(file_path)
        if not file_metadata:
            print(f"  Не удалось извлечь EXIF данные")
            continue
        
        data.append(file_metadata)

    return data

def write_data_to_csv(folder_path, data):
    data.sort(key=lambda x: x['identifier'])
    with open(os.path.join(folder_path, 'metadata.csv'), 'w', newline='', encoding='utf-8') as file:
        if data:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def latitude_to_float(lat_str):
    sign = 1 if lat_str[-1] == 'N' else -1
    degrees, minutes = map(float, lat_str[:-1].split(','))
    lat_float = sign * (degrees + minutes / 60)
    # print(f"Широта: {lat_str} -> {lat_float}")
    return lat_float

def longitude_to_float(lon_str):
    sign = 1 if lon_str[-1] == 'E' else -1
    degrees, minutes = map(float, lon_str[:-1].split(','))
    lon_float = sign * (degrees + minutes / 60)
    # print(f"Долгота: {lon_str} -> {lon_float}")
    return lon_float

def write_ym_csv(folder_path, full_data):
    keys_to_keep = ['Longitude', 'Latitude', 'title', 'description', 'identifier']
    data = [{k: d[k] for k in keys_to_keep if k in d} for d in full_data]
    data.sort(key=lambda x: x['identifier'], reverse=True)

    for row in data:
        row['identifier'] = row['identifier'].split('/')[-1]
        row['Latitude'] = latitude_to_float(row['Latitude'])
        row['Longitude'] = longitude_to_float(row['Longitude'])

    with open(os.path.join(folder_path, 'ym_table.csv'), 'w', newline='', encoding='utf-8') as file:
        new_fieldnames = ['Широта', 'Долгота', 'Описание', 'Подпись', 'Номер метки']
        writer = csv.DictWriter(file, fieldnames=new_fieldnames)
        writer.writeheader()

        mapping = {
            'Latitude': 'Широта',
            'Longitude': 'Долгота',
            'title': 'Описание',
            'description': 'Подпись',
            'identifier': 'Номер метки',
        }

        for row in data:
            writer.writerow({mapping[k]: v for k, v in row.items() if k in mapping})


def latitude_to_text(lat_str):
    direction = lat_str[-1]
    degrees, minutes = map(float, lat_str[:-1].split(','))
    seconds = (minutes - int(minutes)) * 60
    lat_text = f"{int(degrees)}°{int(minutes)}'{seconds:.1f}\"{direction}"
    # print(f"Широта: {lat_str} -> {lat_text}")
    return lat_text

def longitude_to_tex(lon_str):
    direction = lon_str[-1]
    degrees, minutes = map(float, lon_str[:-1].split(','))
    seconds = (minutes - int(minutes)) * 60
    lon_text = f"{int(degrees)}°{int(minutes)}'{seconds:.1f}\"{direction}"
    # print(f"Долгота: {lon_str} -> {lon_text}")
    return lon_text

def write_tg_messages(folder_path, full_data):
    full_data.sort(key=lambda x: x['identifier'])

    with open(os.path.join(folder_path, 'tg_messages.txt'), 'w', encoding='utf-8') as file:
        for row in full_data:
            lat = latitude_to_text(row['Latitude'])
            lon = longitude_to_tex(row['Longitude'])
            date, time = row['DateTimeOriginal'].split(' ')
            date = date.replace(':', '-')
            time = time.split('.')[0]
            lat_f = latitude_to_float(row['Latitude'])
            lon_f = longitude_to_float(row['Longitude'])

            file.write(f"{row['description']}\n\n")
            file.write(f"{row['title']}\n\n")
            file.write(f"{lat} {lon}\n\n")
            file.write(f"https://yandex.ru/maps/?pt={lon_f},{lat_f}&z=18&l=map\n\n")
            file.write(f"{date} {time}\n\n")
            file.write("#календарь2026@potylitcyn\n")
            file.write("Заказать в ВК или купить с Авито Доставкой\n\n")
            file.write("https://vk.com/market/product/kalendar-2026-169046593-13305201\n\n")
            file.write("https://www.avito.ru/dolgoprudnyy/knigi_i_zhurnaly/kalendar_nastennyy_2026_7900365172\n\n")
            file.write(f"---------\n\n")


# Обложка

# Команда мечты на пляже Анс-Патат

# 4°20'16.8"S 55°50'3.5"E
# 2025-11-06 15:54:51

# #календарь2026@potylitcyn
# Заказать в ВК или купить с Авито Доставкой


def write_vk_messages(folder_path, full_data):
    full_data.sort(key=lambda x: x['identifier'])

    with open(os.path.join(folder_path, 'vk_messages.txt'), 'w', encoding='utf-8') as file:
        for row in full_data:
            lat = latitude_to_text(row['Latitude'])
            lon = longitude_to_tex(row['Longitude'])
            date, time = row['DateTimeOriginal'].split(' ')
            date = date.replace(':', '-')
            time = time.split('.')[0]
            lat_f = latitude_to_float(row['Latitude'])
            lon_f = longitude_to_float(row['Longitude'])

            file.write(f"{row['description']}\n\n")
            file.write(f"{row['title']}\n\n")
            file.write(f"{lat} {lon}\n")
            file.write(f"{date} {time}\n\n")
            file.write("#календарь2026@potylitcynblog\n")
            file.write("Заказать в ВК или купить с Авито Доставкой\n")
            file.write("https://www.avito.ru/dolgoprudnyy/knigi_i_zhurnaly/kalendar_nastennyy_2026_7900365172\n\n")
            file.write(f"---------\n\n")

def write_coordinates(folder_path, full_data):
    full_data.sort(key=lambda x: x['identifier'])

    with open(os.path.join(folder_path, 'coordinates.txt'), 'w', encoding='utf-8') as file:
        for row in full_data:
            lat = latitude_to_text(row['Latitude'])
            lon = longitude_to_tex(row['Longitude'])
            date, time = row['DateTimeOriginal'].split(' ')
            date = date.replace(':', '-')
            time = time.split('.')[0]
            lat_f = latitude_to_float(row['Latitude'])
            lon_f = longitude_to_float(row['Longitude'])

            file.write(f"{row['description']} ({row['title']}): {lat} {lon} {date} {time}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Извлечение EXIF данных из фотографий')
    parser.add_argument('folder', help='Путь к папке с фотографиями')
    parser.add_argument('-o', '--output', default='exif_data.csv', 
                       help='Имя выходного CSV файла (по умолчанию: exif_data.csv)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.folder):
        print(f"Ошибка: Папка '{args.folder}' не существует")
        exit(1)
    
    data = read_folder_xmp(args.folder)
    write_data_to_csv(args.folder, data)
    write_ym_csv(args.folder, data)
    write_coordinates(args.folder, data)
    write_tg_messages(args.folder, data)
    write_vk_messages(args.folder, data)