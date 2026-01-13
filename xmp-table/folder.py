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

    data.sort(key=lambda x: x['identifier'])
    with open(os.path.join(folder_path, 'metadata.csv'), 'w', newline='', encoding='utf-8') as file:
        if data:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Извлечение EXIF данных из фотографий')
    parser.add_argument('folder', help='Путь к папке с фотографиями')
    parser.add_argument('-o', '--output', default='exif_data.csv', 
                       help='Имя выходного CSV файла (по умолчанию: exif_data.csv)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.folder):
        print(f"Ошибка: Папка '{args.folder}' не существует")
        exit(1)
    
    read_folder_xmp(args.folder)