import discord
from discord.ext import commands
import json
import atexit
from hasperm import *
from jsonloader import *

class Economy(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.rawconfig = config
        self.config = config['ECONOMY']
        self.data = getfilecontent()

    
#region admin-commands
    @commands.command(brief="Manually registeres a user in the database.", help='<user>')
    async def registeruser(self, ctx, member:discord.Member=None):
        if await has_admin(ctx.message.author, ctx.message.channel, ctx):
            if not member == None:
                if not str(member.id) in self.data:
                    balance = {'balance' : self.config['startbalance']}
                    self.data[str(ctx.guild.id)][str(member.id)] = balance
                    await ctx.send(f'User {member.name} was registered successfully.')
                else:
                    await ctx.send('ERROR\nThe member you wanted to register is already registered.')
            else:
                await ctx.send('Error\nYou need to specify a member.')


    @commands.command(aliases=['addmoney', 'ecogive'], brief="Give someone Money.", help='<amount> <user>')
    async def givemoney(self, ctx, member:discord.Member=None, amount=0):
        if await has_admin(ctx.message.author, ctx.message.channel, ctx):
            amount = int(amount)
            if amount <= 0:
                await ctx.send('You can\'t give someone 0 or less.')
            
            if member == None:
                member = ctx.message.author

            checkuser(member, ctx)
            amount = int(amount)
            self.data[ctx.guild.id][str(member.id)]['balance'] += amount
            await ctx.send(f'You gave {member.name} {amount}{self.config["currency"]}.')

    @commands.command(aliases=['ecoset'], brief="Sets a users balance.", help='<amount> <user>')
    async def setmoney(self, ctx, amount=0, member:discord.Member=None):
        if await has_admin(ctx.message.author, ctx.message.channel, ctx):
            amount = int(amount)
            if amount <= 0:
                await ctx.send('You can\'t give someone 0 or less.')
            
            if member == None:
                member = ctx.message.author
        
            checkuser(member, ctx)
            amount = int(amount)
            self.data[str(member.id)]['balance'] = amount
            await ctx.send(f'Set {member.name}\'s money to {amount}{self.config["currency"]}.')


    @commands.command(aliases=['ecoreset'], brief="Sets a users balance to start balance.", help='<user>')
    async def resetmoney(self, ctx, member:discord.Member=None):
        if await has_admin(ctx.message.author, ctx.message.channel, ctx):
            if member == None:
                member = ctx.message.author
        
            checkuser(member, ctx)
            self.data[str(member.id)]['balance'] = int(self.config['startbalance'])
            await ctx.send(f'Reset {member.name}\'s money.')

    @commands.command(aliases=['ecocurrency'], brief="Changes the currency. WARNING: Some characters may be buggy.", help='<symbol>')
    async def setcurrency(self, ctx, currency):
        if await has_admin(ctx.message.author, ctx.message.channel, ctx):
            self.config['currency'] = currency
            await ctx.send(f'Set currency to \'{currency}\'.')

#endregion
#region user-commands

    @commands.command(aliases=['money', 'bal'], brief="Shows you your balance.", help='<user>')
    async def balance(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.message.author
            prefix = 'You have'
        else:
            prefix = f'{member.name} has'

        checkuser(member, ctx)
        money = self.data[str(ctx.guild.id)][str(member.id)]['balance']
        await ctx.send(f"{prefix} {money}{self.config['currency']}.")

    @commands.command(brief="Pay someone money.", help='<target-user> <amount>')
    async def pay(self, ctx, target:discord.Member=None, amount=0):
        member = ctx.message.author
        if not amount <= 0:
            if not target == None:
                checkuser(target)
                checkuser(member, ctx)
                amount = int(amount)
                if self.data[str(member.id)]['balance'] >= amount:
                    self.data[str(member.id)]['balance'] -= amount
                    self.data[str(target.id)]['balance'] += amount
                    await ctx.send(f'You gave {target.name} {amount}{self.config["ECONOMY"]["currency"]}.')
                else:
                    await ctx.send('You do not have enough money to perfom this action.')
            else:
                await ctx.send('You have to specify a member.')
        else:
            await ctx.send('The amount has to be above zero.')

#endregion
