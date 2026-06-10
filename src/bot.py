from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

import json
from pathlib import Path

from processors.build_generator import getItemsForChampion

#-------- helpers

with open( Path(__file__).resolve().parent.parent / "data" / "name_corrections.json", "r") as f:
    name_corrections = json.load(f)


def normaliseName(champion_name):

    champion_name = champion_name.capitalize().replace("'", "").replace(".", "").replace(" ", "")

    if champion_name in name_corrections:
        champion_name = name_corrections[champion_name]

    return champion_name

# ----- bot stufff

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="l!", intents=intents)

@bot.command()
async def oi(ctx):
    await ctx.send(f"oi {ctx.author.mention}")

@bot.command()
async def papagaio(ctx, msg: str):
    await ctx.send(msg)

@bot.command()
async def versao(ctx):
    msg = """versao alpha 1.1"""
    await ctx.send(msg)

@bot.command()
async def guia(ctx):
    msg = """só da l!build (nome do boneco)
mas tem algumas exceções como:
se o boneco tiver ' no nome, igual o kha'zix, é so manda -> l!build khazix ou l!build kha'zix (mas sem espaco)
se o boneco tiver espaco no nome, igual o master yi, po mandar o nome inteiro, l!build master yi, ou é so mandar o primeiro nome -> l!build master"""
    await ctx.send(msg)

@bot.command()
async def build(ctx, champion_name: str):

    if champion_name == "ehan":
        await ctx.send("o guerreiro nao precisa de items...")

    champion_name = normaliseName(champion_name)

    #console logging
    print(f"Procurando build para: {champion_name}")

    try:
        pre_sorted_item_list = getItemsForChampion(champion_name)
    

        item_list  = dict(sorted(pre_sorted_item_list.items(), key=lambda item: item[1]['PickRate'], reverse=True)) 

        best_items = f"""Melhores items para {champion_name}:"""

        for index, (itemName, itemStats) in enumerate(item_list.items()):
            best_items += f"""\n{index+1}. **{itemName}** *comprado em {itemStats['purchases']} jogos* | **PickRate:** {itemStats['PickRate']}% | **WinRate:** {itemStats['WinRate']}% | """
            if itemStats['WPA'] >= 0: 
                best_items += f"""**WPA:** +{itemStats['WPA']}"""
            else:
                best_items += f"""**WPA:** {itemStats['WPA']}"""

        #ensuring msg is under 2000 char
        if len(best_items) > 2000: 
            best_items = best_items[:2000]
            endIndex = len(best_items)-best_items[::-1].index('.')+2
            best_items = best_items[:endIndex]

        await ctx.send(best_items)

    except KeyError:
        await ctx.send(f"nao achei build para {champion_name}")

@bot.command()
async def wpa(ctx):
    msg = """WPA (Win Probability Added) é a Probabilidade de vitória adicionada\nSignifica o quanto esse item mudou a chances de vitoria\n*WPA = Winrate do item - Winrate do boneco*"""
    await ctx.send(msg)

@bot.command()
async def github(ctx):
    await ctx.send("https://github.com/vitelli55/league-analytics-discord-bot")

bot.run(BOT_TOKEN)
