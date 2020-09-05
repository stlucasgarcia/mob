import discord
from discord.ext import commands, tasks
from intertools import cycle
from commandslist import *

Bot_token = 'NzQ1ODAzOTMxMDk5MzMyNjM4.Xz3GCQ.uUA2Eck1PK1-9pRizBt-gfuRaUQ'
Prefix = 'm-'
client = commands.Bot(command_prefix=Prefix)
status = cycle(['Procurando atualizações...', 'Olhando para o Moodle', 'Descobrindo tarefas'])

@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@tasks.loop(seconds=10)
async def status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(Bot_token)
