import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import *
import datetime
import os
from hasperm import *

class Moderation(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.settings_list = ['prefix', 'username', 'description', 'activity', 'color']

    @commands.command(brief="Change the bot settings.", help='<prefix/username/activity> <argument>')
    async def settings(self, ctx, mode='', arg=''):
        if await has_admin(ctx.message.author, ctx.message.channel, ctx):
            if not mode == '' and not arg == '':
                if mode in self.settings_list:
                    var_name = mode.lower()
                    if mode == 'prefix':
                        self.bot.command_prefix = arg
                    elif mode == 'username':
                        await ctx.guild.me.edit(nick=arg)
                    elif mode == 'activity':
                        await self.bot.change_presence(activity=discord.Game(name=arg))
                        self.config['BOT']['activity'] = arg
                
                print(f'Changed variable \'{var_name}\' to \'{arg}\'.')

                embed = discord.Embed(title=f':gear: Settings', description=f'Changed variable \'{var_name}\' to \'{arg}\'.',
                                      timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                await ctx.send(embed=embed)


    @commands.command(brief="Shows the bot ping.(ms)")
    async def ping(self, ctx):
        await ctx.send(f':ping_pong: Pong! {round(self.bot.latency, 0)}ms')


    @commands.command(brief="Shows server info.")
    async def info(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description="A discord server.",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Server created at",
                        value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        await ctx.send(embed=embed)

    @commands.command(brief="Makes the bot say something.", help='<argument>')
    async def say(self, ctx, *, args=''):
        if args == '':
            await ctx.send('An argument is needed.')
        else:
            await ctx.send(args)

    @commands.command(brief="Restarts the bot.")
    async def restart(self, ctx):
        if await has_admin(ctx.message.author, ctx.message.channel, ctx):
            print('Restarting...')
            await ctx.send('Restarting...')
            await self.bot.close()

# endregion
