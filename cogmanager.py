from reactionrole import ReactionRole
from warnsys import WarnSystem
import discord
from discord.ext import commands


from economy import *
from reactionrole import *
from moderation import *
from logger import *
from worksys import *
from reactionrole import *
from polls import *

class CogManager(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.commands = [Economy, WarnSystem, Moderation, Logger, WorkSystem, ReactionRole, Polls]
        self.load_systems()

    def load_systems(self):
        for command in self.commands:
            self.bot.add_cog(command(self.bot, self.config))