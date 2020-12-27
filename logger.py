import asyncio
import json
import discord.utils
from discord.ext import commands, tasks

class Logger(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config['LOGGING']
        self.guilds = json.loads(self.config.get('guilds'))
        self.test.start()

    def makelog(self):
        self.postlog()

    async def postlog(self):
        await self.bot.send('test')

    @commands.command()
    async def enablelogging(self, ctx, channel: discord.TextChannel):
        self.guilds.append(str(ctx.guild.id))
        self.config.set('guilds', json.dumps(self.guilds))
        print(f'Server {ctx.guild.name} just enabled logging.')
    
    @commands.command()
    async def getlog(self, ctx):
        print('Requesting audit logs')
        await self.save_audit_logs(ctx.guild)

    #async def save_audit_logs(self, guild):
    #    async for entry in guild.audit_logs(limit=100):
    #        file.write(f'{entry.user} did {entry.action} to {entry.target} + {entry.id}\n')

    @tasks.loop(seconds=5)
    async def test(self):
        for id in self.guilds:
            guild = self.bot.get_guild(id)
            with open(f'audit_logs\\{guild.id}.txt', 'w+', encoding='utf-8') as file:
                async for entry in guild.audit_logs(limit=10):
                    print(entry)
