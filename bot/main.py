import discord
from discord.ext import commands, tasks
from itertools import cycle
from commandslist import *
from secret import Bot_token, bitly_token
import pandas as pd
# import bitlyshortener

#short = bitlyshortener.Shortener(tokens=bitly_token, vanitize=True)
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
async def tarefas(ctx):
    database = pd.read_csv(PATH, header=None )
    modulename = ''
    
    # urls = pd.DataFrame(database, columns=['deadline'])
    # print(urls, type(urls))
    for i in range(1,3):# numero de linhas do csv
        if database.iat[i,3] == 'assign':
            modulename = 'Tarefa para entregar via Moodle'
        elif database.iat[i,3] == 'bigbluebutton':
            modulename = 'Aula ao vivo - BigBlueButton'
            
        fullname = database.iat[i,0]
        name = database.iat[i,1]
        description = database.iat[i,2]
        deadline = database.iat[i,4] + ' às ' + database.iat[i,5]
        link = database.iat[i, 6]
        # url = urls[i]
        # print(link, url)
        # print(database)

        embed=discord.Embed(title=modulename, color=0xcc0000)
        embed.set_thumbnail(url="https://logodownload.org/wp-content/uploads/2017/09/mackenzie-logo-3.png")
        embed.add_field(name="Matéria", value=fullname, inline=True)
        embed.add_field(name="Nome da tarefa", value=name, inline=True)
        embed.add_field(name="Descrição", value=description, inline=False)
        embed.add_field(name="Tipo de tarefa", value=modulename, inline=True)
        embed.add_field(name="Data de entrega", value=deadline, inline=True)
        embed.add_field(name="Link", value=link, inline=False)
        embed.set_footer(text="Feito com ❤ por alunos do Mackenzie.")
        
        
        await ctx.send(embed=embed)



client.run(Bot_token)
