import shutil
import sys
import os


# Name paths

catalog_path = sys.argv[1]
raw_path = os.path.join(catalog_path, "RAW")
days = os.listdir(raw_path)[1:]

print("\nCatalog path: ", catalog_path)
print("RAW path: ", raw_path)
print("Days:", days)

photo_path = os.path.join(catalog_path, "photo")
src_path = os.path.join(photo_path, 'src')
pro_path = os.path.join(photo_path, 'pro')

print("Photo path:", photo_path)
print("Src path:", src_path)
print("Pro path:", pro_path)


# Create folders

os.mkdir(photo_path)
os.mkdir(src_path)
os.mkdir(pro_path)


# Delete backups

bkp_folder = 'lrcat_backup'
if bkp_folder in os.listdir(catalog_path)[1:]:
    print("Delete backups from", bkp_folder)
    shutil.rmtree(os.path.join(catalog_path, bkp_folder))
else:
    print("Error! No backup folder in the catalog!")


# Move sources

for day in days:
    print("\nWorking with", day)

    day_path = os.path.join(raw_path, day)
    print("Day path:", day_path)

    day_ymd = day.split('-')
    new_day = day_ymd[1] + '.' + day_ymd[2]
    new_day_path = os.path.join(src_path, new_day)
    print("New day path:", new_day_path)

    rename_from_path = os.path.join(new_day_path, day)
    raname_to_path = os.path.join(new_day_path, "C5DM4")
    print("Rename from", rename_from_path, "to", raname_to_path)

    os.mkdir(new_day_path)
    shutil.move(day_path, new_day_path)
    os.rename(rename_from_path, raname_to_path)


# Move catalog to a pro folder

files = os.listdir(catalog_path)[1:]

for file in files:
    if file.endswith(".lrcat"):
        catalog_path = os.path.join(catalog_path, file)
        new_catalog_path = os.path.join(pro_path, file)
        print("\nMove catalog from", catalog_path, "to", new_catalog_path)

        shutil.move(catalog_path, new_catalog_path)


# Delete RAW folder

print("\nDelete RAW folder from ", raw_path)
shutil.rmtree(raw_path)

print("\nRefoldering of the", catalog_path, "done.")
