import discord
from discord.ext import commands, tasks
from itertools import cycle
from commandslist import *
from secret import Bot_token
import pandas as pd


Prefix = 'm-'
client = commands.Bot(command_prefix=Prefix)
status = cycle(['Procurando atualizações...', 'Olhando para o Moodle', 'Descobrindo tarefas', 'Destruindo a casa do Jamil'])
PATH = r'C:\Users\lukep\Documents\Projects\Discord Bot\DiscordMackBot\template.csv'


@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))


@tasks.loop(seconds=10)
async def change_status():
    # print("next status")
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def clear(ctx, amount=10):
    print("clear command")
    await ctx.channel.purge(limit=amount)


@client.command()
async def print_data(ctx):
    database = pd.read_csv(PATH, header=None )

    for i in range(1,3):# numero de linhas do csv
        if database.iat[i,3] == 'assign':
            database.iat[i,3] = 'Tarefa para entregar'
        elif database.iat[i,3] == 'bigbluebutton':
            database.iat[i,3] = 'Aula ao vivo - BigBlueButton'
            
        fullname = database.iat[i,0]
        name = database.iat[i,1]
        description = database.iat[i,2]
        modulename = database.iat[i,3]
        deadline = database.iat[i,4] + ' às ' + database.iat[i,5]
        link = database.iat[i, 6]
        embed=discord.Embed(title=modulename, color=0xcc0000)
        embed.set_thumbnail(url="https://logodownload.org/wp-content/uploads/2017/09/mackenzie-logo-3.png")
        embed.add_field(name="Matéria", value=fullname, inline=True)
        embed.add_field(name="Nome da tarefa", value=name, inline=True)
        embed.add_field(name="Descrição", value=description, inline=True)
        embed.add_field(name="Tipo de tarefa", value=modulename, inline=True)
        embed.add_field(name="Data de entrega", value=deadline, inline=True)
        embed.add_field(name="Link", value=link, inline=False)
        embed.set_footer(text="Feito com ❤ por alunos do Mackenzie.")
        await ctx.send(embed=embed)
    # for i in range(1,3):# numero de linhas do csv
    #     msg = '>>> '
    #     for j in range(6): # numero de colunas do csv
            
    #         if database.iat[i,3] == 'assign':
    #             database.iat[i,3] = 'Tarefa'
    #         elif database.iat[i,3] == 'bigbluebutton':
    #             database.iat[i,3] = 'Aula - BigBlueButton'

    #         msg += str(database.iat[i,j]) + "\n"
    #     print(database.iat[i,3])
    #     await ctx.channel.send(msg)
    #     await ctx.channel.send(embed=colors)


"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return
"""


client.run(Bot_token)
