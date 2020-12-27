import discord

def isAdmin(self, member: discord.Member):
    if member.has_permission(admin=True):
        print('has perm')
