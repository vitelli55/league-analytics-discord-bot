import requests
import os
import json
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv()
RIOT_API = os.getenv("RIOT_API")

data_folder_location = Path(__file__).resolve().parent.parent.parent / "data"
match_list_location = data_folder_location / "matchesId_list.json"

with open(match_list_location, "r") as file:
   all_matches = json.load(file)


def getMatchInfo(match_id):
    request_link = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API}"
    reponse = requests.get(request_link)
    match_info = reponse.json()

    return match_info

def isMatchInFolder(match_id) -> bool:
    match_path = data_folder_location / "raw_matches" / f"{match_id}.json"

    if match_path.exists():
        return True
    else:
        return False
    
def isValidRequest(data) -> bool:
    if 'status' in data:
        return False
    else: 
        return True

def saveMatchInfo(id, match_id):

    if isMatchInFolder(match_id):
        print(f"Match already in folder. Skipping...")
    else:
        files_dir = data_folder_location / "raw_matches" / f"{match_id}.json"

        print(f"File {id} out of {len(all_matches)}. Storing information for match {match}")
        data = getMatchInfo(match)

        if isValidRequest(data) == False: #if the request exceeds api limit, wait a bit and request again
            time.sleep(2.3)
            data = getMatchInfo(match)

        with open(files_dir, "w") as f:
            json.dump(data, f)


#------------

for id, match in enumerate(all_matches):
    
    saveMatchInfo(id, match)
    #time.sleep(1.3)

