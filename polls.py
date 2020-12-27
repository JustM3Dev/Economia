import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import *
import datetime
from hasperm import *

class Polls(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.question = ''
        self.channel = None
        self.msg = None
        self.cross = self.bot.get_emoji(772900239517417523)

    @commands.command(aliases=['cp'], brief='Create a new poll.', help='<question>')
    async def createpoll(self, ctx, *, question):
        if has_admin(ctx.message.author, ctx.messsage.channel, ctx):
            self.channel = ctx.message.channel
            self.question = question

            embed = discord.Embed(title=self.question, description='How to vote:\n:white_check_mark: = Yes\n<:crossmark:772900239517417523> = No', timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            self.msg = await self.channel.send(embed=embed)
            await self.msg.add_reaction('✅')
            await self.msg.add_reaction(self.cross)
        
    @commands.command(aliases=['pr'], brief='Get the poll results.')
    async def pollresults(self, ctx):
        if has_admin(ctx.message.author, ctx.messsage.channel, ctx):
            if self.msg:
                lock = self.bot.get_emoji(778287269022269466)
                self.msg = await self.channel.fetch_message(self.msg.id)

                yes_reactions = get(self.msg.reactions, emoji='✅')
                yes_reactions = yes_reactions.count - 1
                no_reactions = get(self.msg.reactions, emoji=self.cross)
                no_reactions = no_reactions.count - 1
                total_reactions = yes_reactions + no_reactions

                try:
                    yes_percentage = round((yes_reactions / total_reactions) * 100, 0)
                except ZeroDivisionError:
                    yes_percentage = 0

                try:
                    no_percentage = round((no_reactions / total_reactions) * 100, 0)
                except ZeroDivisionError:
                    no_percentage = 0

                embed = discord.Embed(title=f'[LOCKED] {self.question}', description='This poll is already finished.\nMaybe you are lucky next time!', timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                await self.msg.edit(embed=embed)
                await self.msg.add_reaction('\N{LOCK}')

                embed = discord.Embed(title='Poll results', description=f'{ctx.message.author.mention} started a poll. Here are the results:', timestamp=datetime.datetime.utcnow(), color=discord.Color.green()) 
                
                if not yes_percentage == 0 and not no_percentage == 0:
                    embed.add_field(name='Yes', value=f'Count: {yes_reactions}\nPercentage: {yes_percentage}')
                    embed.add_field(name='No', value=f'Count: {no_reactions}\nPercentage: {no_percentage}')
                else:
                    embed.add_field(name='Oh...', value=f'Noone reacted so we couldn\'t process anything.')

                await ctx.send(embed=embed)
            else:
                await ctx.send('<:crossmark:772900239517417523> Oh... It seems like you forgot to create a poll.')
