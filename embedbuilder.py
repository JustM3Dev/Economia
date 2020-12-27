import discord
from discord import Color
import datetime
import random
from embedbuilderexceptions import *

colors = [discord.Color.teal, discord.Color.dark_teal, discord.Color.green, discord.Color.dark_green, discord.Color.blue,discord.Color.dark_blue,discord.Color.purple,discord.Color.dark_purple,discord.Color.magenta,discord.Color.dark_magenta,discord.Color.gold,discord.Color.dark_gold,discord.Color.orange,discord.Color.dark_orange,discord.Color.red,discord.Color.dark_red,discord.Color.lighter_grey,discord.Color.dark_grey,discord.Color.light_grey,discord.Color.darker_grey,discord.Color.blurple,discord.Color.greyple]
gen_embed = None

def embed(title, description='', time=datetime.datetime.utcnow(), color=random.choice(colors),footer_text='ModPlus', footer_icon='https://cdn.discordapp.com/app-icons/771921393976868884/13a73a6ed80797fcfd04cf94127dfb1f.png?size=256'):
    global gen_embed
    gen_embed = discord.Embed(title=title, description=description, timestamp=time)
    gen_embed.set_footer(text=footer_text, icon_url=footer_icon)

def add_field(title='', content='', inline=False):
    global gen_embed
    if title or content:
        gen_embed.add_field(name=title, value=content)
    else:
        raise ValueError()

def get_embed():
    global gen_embed
    return gen_embed
    