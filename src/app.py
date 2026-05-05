from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

from scrapper import get_build

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

    # ---- few exceptions
    if champion_name in ['master', 'Master', 'yi', 'Yi']:
        champion_name = "master yi"
    elif champion_name in ['Twisted', 'twisted']:
        champion_name = "twisted fate"
    elif champion_name in ['Miss', 'miss']:
        champion_name = "miss fortune"
    elif champion_name in ['Aurelion', 'aurelion']:
        champion_name = "aurelion sol"
    elif champion_name in ['dr', 'Dr', 'dr.', 'Dr.', 'mundo', 'Mundo']:
        champion_name = "dr mundo"
    elif champion_name in ['jarvan', 'Jarvan']:
        champion_name = "JarvanIV"
    

    item_list = get_build(champion_name)
    
    if not item_list:
        await ctx.send(f"nao achei build para {champion_name}")
    else:
        await ctx.send(f"build para {champion_name}: {item_list}")



bot.run(BOT_TOKEN)
