import requests
import os
from dotenv import load_dotenv

load_dotenv()
RIOT_API = os.getenv("RIOT_API")

team_colour = {
    100: "blue",
    200: "red"
}

queue_ids = {
    420: "ranked_soloduo",
    440: "ranked_flex"
}

rank_to_number = {
    ("IRON", "IV"): 1,
    ("IRON", "III"): 2,
    ("IRON", "II"): 3,
    ("IRON", "I"): 4,
    ("BRONZE", "IV"): 5,
    ("BRONZE", "III"): 6,
    ("BRONZE", "II"): 7,
    ("BRONZE", "I"): 8,
    ("SILVER", "IV"): 9,
    ("SILVER", "III"): 10,
    ("SILVER", "II"): 11,
    ("SILVER", "I"): 12,
    ("GOLD", "IV"): 13,
    ("GOLD", "III"): 14,
    ("GOLD", "II"): 15,
    ("GOLD", "I"): 16,
    ("PLATINUM", "IV"): 17,
    ("PLATINUM", "III"): 18,
    ("PLATINUM", "II"): 19,
    ("PLATINUM", "I"): 20,
    ("EMERALD", "IV"): 21,
    ("EMERALD", "III"): 22,
    ("EMERALD", "II"): 23,
    ("EMERALD", "I"): 24,
    ("DIAMOND", "IV"): 25,
    ("DIAMOND", "III"): 26,
    ("DIAMOND", "II"): 27,
    ("DIAMOND", "I"): 28,
    ("MASTER", "I"): 29,
    ("GRANDMASTER", "I"): 30,
    ("CHALLENGER", "I"): 31
}

number_to_rank = {v: k for k, v in rank_to_number.items()}

def getMatchIDByPuuid(puuid):
    request_link = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={RIOT_API}"

    response = requests.get(request_link)
    matches = response.json()

    return matches

def getPuuids(league):
    # leagues = ['challengerleagues', 'grandmasterleagues', 'masterleagues']
    challenger_league = f"https://br1.api.riotgames.com/lol/league/v4/{league}/by-queue/RANKED_SOLO_5x5?api_key={RIOT_API}"

    response = requests.get(challenger_league)
    puuids = [entry['puuid'] for entry in response.json()['entries']]

    return puuids

def getIndividualSoloRank(puuid):
    request_link = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={RIOT_API}"
    response = requests.get(request_link)
    account_info = response.json()

    solo_rank = None

    for entry in account_info:
        if entry['queueType'] == "RANKED_SOLO_5x5":
            solo_rank = (entry['tier'], entry['rank'])

    return solo_rank
    
def getIndividualFlexRank(puuid):
    request_link = f"https://br1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={RIOT_API}"
    response = requests.get(request_link)
    account_info = response.json()  

    flex_rank = None

    for entry in account_info:
        if entry['queueType'] == "RANKED_FLEX_SR":
            flex_rank = (entry['tier'], entry['rank'])
    
    return flex_rank

# --- calculating average rank of a match

def getAverageRank(match_info):
    match_puuids = match_info['metadata']['participants']

    players_ranks = []

    if match_info['info']['queueId'] == 420: #its ranked solo
        for puuid in match_puuids:
            players_ranks.append(getIndividualSoloRank(puuid))
    elif match_info['info']['queueId'] == 440: #its ranked flex
        for puuid in match_puuids:
            players_ranks.append(getIndividualFlexRank(puuid))

    sum = 0
    for rank in players_ranks:
        sum = sum + rank_to_number[rank]

    average = sum/len(players_ranks) if len(players_ranks) != 0 else 0

    rank_average = number_to_rank[round(average)]
    return rank_average

# ---- displaying match info 

def getMatchInfo(match_id):
    request_link = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API}"
    reponse = requests.get(request_link)
    match_info = reponse.json()

    team_info = match_info['info']['teams'] #list with 2 elements (2 dictionaries)

    info_dic = {
        "match_duration": f"{round(match_info['info']['gameDuration']/60)} minutes" ,
        "result": "blueWins" if team_info[0]['win'] else "redWins",
        "averageRank": getAverageRank(match_info),
        "queueType": queue_ids[match_info['info']['queueId']]


    }

    return info_dic



my_puuid = 'jLMkZ05nkw1LwfHuEWC3OsIVm8XSPPQNEYGfejtSzZUxDARTUxgMELYhbZN1B9R47HBBEE636ZVM0Q'
most_recent_match = getMatchIDByPuuid(my_puuid)[0]

# example of my last 20 ranked solo matches: 
# https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{my_puuid}/ids?queue=420&type=ranked&start=0&count=20&api_key={RIOT_API}

#print(getIndividualSoloRank(my_puuid))
top_3_leagues_puuid = getPuuids('challengerleagues') + getPuuids('grandmasterleagues') + getPuuids('masterleagues')
print(len(top_3_leagues_puuid))



#match_id = getMatchIDByPuuid(getPuuids()[0])[0]
#print(getMatchResult(match_id))

#print(getPuuids()[:1])

