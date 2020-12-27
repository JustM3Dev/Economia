import discord
from discord.ext import commands
from jsonloader import *

class WarnSystem(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.rawconfig = config
        self.config = config['WARN']
        self.data = getfilecontent()

    @commands.command(aliases=['setwarns'], brief="Set warns for a user to x.", help='<user> <amount>')
    async def setwarn(self, ctx, member:discord.Member=None, amount=0):
        if not member == None:
            if amount >= 0:
                checkuser(member)
                self.data[str(member.id)]['warns'] = amount
                await ctx.send(f'Set {member.name}\'s warns to {amount}.')
            else:
                await ctx.send('The amount cant be zero.')
        else:
            await ctx.send('You need to specify a member.')

    @commands.command(aliases=['givewarns'], brief="Add a warn to someone.", help='<user> <amount>')
    async def givewarn(self, ctx, member:discord.Member=None, amount=1):
        if not member == None:
            checkuser(member)
            self.data[str(member.id)]['warns'] += amount
            await ctx.send(f'User {member.name} now has {self.data[str(member.id)]["warns"]} warns.')
        else:
            await ctx.send('You need to specify a member.')

    @commands.command(aliases=['removewarns'], brief="Remove a warn from someone.", help='<user> <amount>')
    async def removewarn(self, ctx, member:discord.Member=None, amount=1):
        if not member == None:
            checkuser(member)
            self.data[str(member.id)]['warns'] -= amount
            await ctx.send(f'User {member.name} now has {self.data[str(member.id)]["warns"]} warns.')
        else:
            await ctx.send('You need to specify a member.')

    @commands.command(aliases=['checkwarns'], brief="Lets you check how many warns someone has.", help='<user>')
    async def checkwarn(self, ctx, member:discord.Member=None):
        if not member == None:
            checkuser(member)
            data = self.data[str(member.id)]['warns']
            await ctx.send(f'User {member.name} has {data} warns.')
        else:
            await ctx.send('You need to specify a member.')

    @commands.command(aliases=['resetwarns'], brief="Resets a users warns to zero.", help='<user>')
    async def resetwarn(self, ctx, member:discord.Member=None):
        if not member == None:
            checkuser(member)
            self.data[str(member.id)]['warns'] = 0
            await ctx.send(f'Set {member.name} warns to zero.')
        else:
            await ctx.send('You need to specify a member.')

    