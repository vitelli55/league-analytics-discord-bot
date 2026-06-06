import json
from pathlib import Path
#from pprint import pprint

CHAMPION_STATS_FILE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "champion_item_stats.json"
ITEMS_ID_FILE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "item_ids" / "item_PTBR.json"

# loading champion stats file
with open(CHAMPION_STATS_FILE_PATH, "r") as f:
    champion_stats = json.load(f)

#loading items ids file, using utf-8 because cp1252 wasnt working
with open(ITEMS_ID_FILE_PATH, "r", encoding="utf-8") as f: 
    item_ids = json.load(f)

# filters:
# purchaseCount > 80

def findItem(item_id):
    return item_ids['data'][item_id]['name']


def getItemsForChampion(champion, MIN_MATCHES=100):

    stats = {}

    for itemID, itemRawInfo in champion_stats[champion]['itemsBought'].items():

        if itemRawInfo['purchaseCount'] < MIN_MATCHES:
            continue


        itemName = findItem(itemID)
        championWR = (champion_stats[champion]['totalWins']/champion_stats[champion]['matchAppearances'])*100
        winRate = (itemRawInfo['winCount']/itemRawInfo['purchaseCount'])*100
        pickRate = (itemRawInfo['purchaseCount']/champion_stats[champion]['matchAppearances'])*100
        wpa = winRate - championWR

        itemInfo = {
            "purchases": itemRawInfo['purchaseCount'],
            "PickRate": round(pickRate,2),
            "WinRate": round(winRate,2),
            "WPA": round(wpa,2)
        }

        #print(f"{findItem(itemID)} | Purchases: {itemInfo['purchaseCount']} | Winrate: {round(winRate,2)} | WPA: {round(wpa,2)}" )

        stats[itemName] = itemInfo

    return stats

# for key, val in champion_stats.items():
#     print(key)
#champion = 'Garen'
#pprint(getItemForChampion(champion))
# for i in champion_stats[champion]['itemsBought']:

#     items = champion_stats[champion]['itemsBought'][i]
#     if items['purchaseCount'] < 100:
#         continue
    
#     championWR = (champion_stats[champion]['totalWins']/champion_stats[champion]['matchAppearances'])*100
#     winRate = (items['winCount']/items['purchaseCount'])*100
#     wpa = winRate - championWR

#     print(f"{findItem(i)} | Purchases: {items['purchaseCount']} | Winrate: {round(winRate,2)} | WPA: {round(wpa,2)}" )

# for i, (key, val) in enumerate(champion_stats[champion]['itemsBought'].items()):

#     item = val
#     if item['purchaseCount'] < 100:
#         continue
    
#     championWR = (champion_stats[champion]['totalWins']/champion_stats[champion]['matchAppearances'])*100
#     winRate = (item['winCount']/item['purchaseCount'])*100
#     wpa = winRate - championWR

#     print(f"{findItem(key)} | Purchases: {item['purchaseCount']} | Winrate: {round(winRate,2)} | WPA: {round(wpa,2)}" )