import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import *
import datetime
import json
import re

class ReactionRole(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.bot_config = config['BOT']
        self.contenttitle = ''
        self.contentdesc = ''
        self.msgs = json.loads(self.config.get('BOT', 'react_msgs'))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = await guild.fetch_member(payload.user_id)

        if str(message.id) in self.msgs:
            if str(payload.emoji) in self.msgs[str(message.id)]:
                print(self.msgs[str(message.id)][str(payload.emoji)])
                role = guild.get_role(int(self.msgs[str(message.id)][str(payload.emoji)]))
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = await guild.fetch_member(payload.user_id)

        if str(message.id) in self.msgs:
            if str(payload.emoji) in self.msgs[str(message.id)]:
                print(self.msgs[str(message.id)][str(payload.emoji)])
                role = guild.get_role(int(self.msgs[str(message.id)][str(payload.emoji)]))
                await member.remove_roles(role)

    @commands.command(aliases=['crr', 'mrr'], brief='Use this command in order to create a new reactionrole.', help='<channel> <msg>')
    async def makereactionrole(self, ctx, channel: discord.TextChannel, *, msg=''):
        if channel != None:
            if msg != None:
                msg = msg.split('|')
                self.contenttitle = msg[0]
                self.contentdesc = msg[1]
                await ctx.send(f'Nice! Now we just need a reaction.\nSyntax: {self.bot_config["prefix"]}rrr <Emoji> <Role>\nSeperate with \', \'\nFor Example: {self.bot_config["prefix"]}rrr :watermelon: @role, :anatomical_heart: @otherrole')
            else:
                await ctx.send(f'You have to specify a message.\nSyntax: {self.bot_config["prefix"]}mrr <channel> <title>|<description>')
        else:
            await ctx.send(f'You have to specify a channel.\nSyntax: {self.bot_config["prefix"]}mrr <channel> <title>|<description>')

    @commands.command(aliases=['rrr'], brief='Use this command in order to set the reactionrole up.\nNOTE: Use makereactionrole before this.', help='<content(seperate with |)>')
    async def reactionrolerole(self, ctx, *, msgcontent):
        msgcontent = msgcontent.split(', ')

        if msgcontent:
            embed = discord.Embed(title=self.contenttitle, description=self.contentdesc, timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            msg = await ctx.send(embed=embed)

            emoji_role = {}
            for item in msgcontent:
                (emoji, role) = item.strip().split(' ')
                print(role)
                ri = re.compile('<@&([0-9]+)>')
                ri = ri.match(role).group(1)
                if ri:
                    emoji_role[emoji] = ri
                    await msg.add_reaction(emoji=emoji)
            self.msgs[str(msg.id)] = emoji_role
            print(json.dumps(self.msgs, indent=2))
            self.config.set('BOT', 'react_msgs', json.dumps(self.msgs))

    @commands.command(brief='Get the last message a user sent.', help='<user>')
    async def lastmessage(self, ctx, user: discord.User):
        oldestMessage = None
        for channel in ctx.guild.text_channels:
            fetchMessage = await channel.history().find(lambda m: m.author.id == user.id)
            if fetchMessage is None:
                continue

            if oldestMessage is None:
                oldestMessage = fetchMessage
            else:
                if fetchMessage.created_at > oldestMessage.created_at:
                    oldestMessage = fetchMessage

        if oldestMessage is not None:
            await ctx.send(f"Last message from {user.name}:\n```{oldestMessage.content}```")
        else:
            await ctx.send("No message found.")