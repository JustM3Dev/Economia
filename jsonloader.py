import json
import atexit
import discord
from jsonloaderexceptions import *
from configmanager import config

filename = 'data.json'
data = {}
print(data)

def readfile():
    global filename, data
    
    with open(filename, "r") as read_file:
        return json.load(read_file)

def getfilecontent():
    global data
    return data

def checkuser(member:discord.Member=None, ctx=None):
    global data

    if not member == None or not ctx == None:
        if not str(member.id) in data:
            jsondata = {'balance' : int(config['ECONOMY']['startbalance']), 'warns' : 0}
            data[ctx.guild.id][str(member.id)] = jsondata
            print(f'User {member.name} was registered successfully.')
    else:
        raise TargetError()

def savefile():
    global filename, data

    with open(filename, "w") as write_file:
        json.dump(data, write_file)

atexit.register(savefile)
data = readfile()
print(data)