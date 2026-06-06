import json
import os
from pathlib import Path
#import pprint

CURRENT_PATCH = "patch16_9"

data_path =  Path(__file__).resolve().parent.parent.parent / "data" 
raw_matches_dir = data_path / "raw_matches" / CURRENT_PATCH
stats_file_path = data_path / "processed" / "champion_item_stats.json"

champion_stats = {}

def getParticipantsInfo(match_data: dict) -> dict:

    participants = match_data['info']['participants']

    match_stats = {}

    for participant in participants:
        champion_played = participant['championName']
        itemsBought = set(participant['challenges']['legendaryItemUsed'])
        match_result = participant['win']

        match_stats[champion_played] = {
            'legendaryItems': itemsBought,
            'win' : match_result
        }

    return match_stats

def updateChampStats(match_data):

    match_stats = getParticipantsInfo(match_data)

    for champion, data in match_stats.items():

        if champion not in champion_stats:
            champion_stats[champion] = {
                'itemsBought': {},
                'matchAppearances': 0,
                'totalWins' : 0
            }
        
        if champion in champion_stats:
            
            # incrementing match appearances
            champion_stats[champion]['matchAppearances'] += 1

            if data['win'] == True:
                champion_stats[champion]['totalWins'] += 1



            for item in data['legendaryItems']:
                if item not in champion_stats[champion]['itemsBought']:
                    champion_stats[champion]['itemsBought'][item] = {'purchaseCount': 0, 'winCount': 0}

                champion_stats[champion]['itemsBought'][item]['purchaseCount'] += 1 

                if data['win'] == True:
                    champion_stats[champion]['itemsBought'][item]['winCount'] += 1

def saveStats():
    with open(stats_file_path, "w") as f:
        json.dump(champion_stats, f, indent=4)


# plan: iterate through every match - os.scandir is faster for 
# if champion is not in the dictionary, create a slot for it.


raw_matches_list = os.listdir(raw_matches_dir)

for id, entry in enumerate(raw_matches_list):

    print(f"File {id} out of {len(raw_matches_list)}. Storing information for match {entry}")
    
    with open(raw_matches_dir/entry, "r") as f:
        match_json = json.load(f)

    updateChampStats(match_json)

    if id%2000==0:
        saveStats()


# -------- testing with 10 matches

# test_list = os.listdir(raw_matches_dir)[:10]

# for entry in test_list:

#     with open(raw_matches_dir/entry, "r") as f:
#         match_json = json.load(f)
    
#     updateChampStats(match_json)

# pprint.pprint(champion_stats)

# with open(stats_file_path, "w") as f:
#     json.dump(champion_stats, f, indent=4)