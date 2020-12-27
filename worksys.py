from discord.ext import *

class WorkSystem(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config