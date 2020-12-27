import asyncio
import discord
from discord.ext import commands
from discord.guild import Guild

async def has_admin(member: discord.Member, channel: discord.TextChannel, ctx):
    if channel.permissions_for(member).administrator:
        return True
    else:
        await ctx.send(':x: Insufficient permissions.')
        return False

async def is_legit(member: discord.Member, ctx):
    if not ctx == None:
        channel = ctx.message.channel
        role = discord.utils.find(lambda r: r.name == 'Legit RP Player', ctx.message.server.roles)

        if role in member.roles:
            return True
        else:
            await ctx.send(':x: Insufficient permissions.')
            return False