#!/usr/bin/python -u
# region import, variables
import configparser
import discord
import datetime

from cogmanager import *
from configmanager import *

config = getconfig()
bot_config = config['BOT']

bot = commands.Bot(command_prefix=bot_config['prefix'],
                   description=bot_config['description'], help_command=None)
# endregion


@bot.event
async def on_ready():
    # region Cogs
    print('Initializing Cogs...')
    bot.add_cog(CogManager(bot, config))
    
    # endregion
    await bot.change_presence(activity=discord.Game(name=bot_config['activity']))
    print('Bot started successfully.')


@bot.command(name="help", brief="Shows a list of all commands.", help='<command>')
async def help(ctx, arg = ''):
    

    if not arg:
        embed = discord.Embed(title=f':gear: Help', description=bot.description,
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        for command in bot.commands:
            embed.add_field(name=command, value=command.brief)
            embed.set_footer(text=f'Use \'{bot_config["prefix"]}\'help <command> for more information about a command.',
                             icon_url="https://images.emojiterra.com/google/android-11/128px/2699.png")
        await ctx.send(embed=embed)
    else:
        for command in bot.commands:
            if str(command) == arg:
                embed = discord.Embed(title=f':gear: Help \'{command}\'', description=command.brief,
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                if command.help == None:
                    command.help = ''
                embed.add_field(name='Usage', value=f'{bot_config["prefix"]}{arg} {command.help}')
                embed.add_field(name='Aliases', value=', '.join(command.aliases))
                await ctx.send(embed=embed)

try:
    print('Starting systems ...')
    bot.run(bot_config['token'])
    print('Done!')
except Exception as e:
    print(f'end: {e}')
