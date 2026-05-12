import os
import json
from pathlib import Path

raw_data_folder_location = Path(__file__).resolve().parent.parent.parent / "data" / "raw_matches"
#matches_location = Path(__file__).resolve().parent.parent.parent / "data" / "raw_matches" / "test.json"

counter = 0
def deleteBadFile(match_id):
    match_path = raw_data_folder_location / f"{match_id}"

    with open(match_path, "r") as file:
        file_to_del = json.load(file)

    if 'status' in file_to_del:
       os.remove(match_path)
       print(f"File {match_id} removed. -> {file_to_del['status']}")
       global counter
       counter = counter + 1
    #else:
        #print("File is all good! No deletion")

for entry in os.scandir(raw_data_folder_location):
    deleteBadFile(entry.name)
print(f"Total files deleted: {counter}")
