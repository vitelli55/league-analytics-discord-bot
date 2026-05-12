import requests
import os
import json
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv()
RIOT_API = os.getenv("RIOT_API")

# top leagues: challengerleagues, grandmasterleagues, masterleagues
# there's 8,409 puuids for the big 3
# rough estimate of matches if we get 20 recent matches 

# 20 ranked solo matches: 
# https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=20&api_key={RIOT_API}

def getTopPuuids(queue) -> list:
    league = f"https://br1.api.riotgames.com/lol/league/v4/{queue}/by-queue/RANKED_SOLO_5x5?api_key={RIOT_API}"

    response = requests.get(league)
    puuids = [entry['puuid'] for entry in response.json()['entries']]

    return puuids

def getMatchIDByPuuid(puuid):
    '''Returns a list of the last 20 SOLO/DUO ranked matches of a player by their puuid'''

    request_link = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=20&api_key={RIOT_API}"

    response = requests.get(request_link)
    matches = response.json()

    return matches

all_matches = set() # a set automatically ensures there's no duplicates
seen_puuids = set() # a list of seen puuids reduces api calls.

all_puuids = getTopPuuids('challengerleagues') + getTopPuuids('grandmasterleagues') + getTopPuuids('masterleagues')
time.sleep(5)

#queues = ['challengerleagues', 'grandmasterleagues', 'masterleagues']

#for queue in queues:
    
#puuids = getTopPuuids(queue)
#print(f"Analysing {len(puuids)} puuids for the queue: {queue}")

print(f"Analysing {len(all_puuids)} puuids")

for id, puuid in enumerate(all_puuids): 
    
    if puuid in seen_puuids:
        print("Puuid already analysed, skipping iteration")
        continue

    seen_puuids.add(puuid)

    print(f"Player {id} out of {len(all_puuids)}. Analysing match history for player {puuid}...")

    matches = getMatchIDByPuuid(puuid)
    all_matches.update(matches)
    print(f"Current size of matches set: {len(all_matches)}")
    time.sleep(1.3)

print("-------------------")
print(f"Finished populating the matches set, final size: {len(all_matches)}, storing a list of match ids in /data/matchesId_list.json")

all_matches_dir = Path(__file__).resolve().parent.parent.parent / "data" / "matchesId_list.json"
with open(all_matches_dir, "w") as f:
    json.dump(list(all_matches), f)

#---------------

