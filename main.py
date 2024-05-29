import discord
from discord.ext import commands
import os
import urllib.request
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Union

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.typing = True

bot = commands.Bot(command_prefix='.', case_insensitive = True, intents=intents)

load_dotenv()
discord_token= os.getenv('discord_token')

async def carregar_comandos():
    for arquivo in os.listdir('Comandos'):
        if arquivo.endswith('.py'): 
           await bot.load_extension(f'Comandos.{arquivo[:-3]}')

async def carregar_ia():
    for arquivo in os.listdir('AI'):
        if arquivo.endswith('.py'): 
           await bot.load_extension(f'AI.{arquivo[:-3]}') 

async def carregar_music():
    for arquivo in os.listdir('Music'):
        if arquivo.endswith('.py'): 
           await bot.load_extension(f'Music.{arquivo[:-3]}')

@bot.event
async def on_ready():
    await carregar_comandos()
    await carregar_music()
    await carregar_ia()
    print(f'{bot.user} está pronto para servir!')   

@bot.command()
async def sync(ctx: commands.Context):
    await ctx.defer(ephemeral=True)
    allowed_ids = [70121026991685663,1215101248051871785 , 365976506473644044, 848296948264075334, 539902997568946186, 366295924370178053]
    if ctx.author.id in allowed_ids:
        sincs = await bot.tree.sync()
        await ctx.reply(f"{len(sincs)} comandos sincronizados")
    else:
        await ctx.reply('Apenas familia pode usar esse comando (ChatGPT, Duardo e Trepoxs)')       

bot.run(discord_token)