import requests 
from bs4 import BeautifulSoup

import json
from pathlib import Path

# ---- HELPER FUNCTIONS

def get_website_content(name):
    champion_name = name
    URL = f"https://probuilds.net/champions/details/{champion_name}/"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    
    return response

# --- LOADING FILES

itemsjson_path = Path(__file__).resolve().parent.parent / "data" / "items.json"

with open(itemsjson_path, "r", encoding="utf-8") as f:
    item_dic = json.load(f)


def get_build(champion_name: str):
    # --- GETTING CHAMPION NAME

    if champion_name != "JarvanIV":
        champion_name = champion_name.capitalize()

    if " " in champion_name:
        champion_name = champion_name.title()
        champion_name = champion_name.replace(" " ,"")
    elif "'" in champion_name:
        champion_name = champion_name.replace("\'", "")    

    print(f"procurando build para {champion_name}...")

    # ---- SCRAPING

    response = get_website_content(champion_name)
    soup = BeautifulSoup(response.content, "html.parser")

    div_stat = soup.find_all("div", class_="stat")
    common_items = None
    items_list = []

    for stat in div_stat:

        label = stat.find("div", class_="label")
        if label and label.get_text(strip=True) == "Common Items":
            common_items = stat
            break
        
    if common_items is not None:
        items = common_items.find_all("div", class_="item")

        for item in items:
            img = item.find("img")
            src = img.get("src")

            if src in item_dic:
                items_list.append(item_dic[src])
            else:
                items_list.append("Unkown Item")
    else: 
        print("Common items not found")


    #print(items_list)
    return items_list



