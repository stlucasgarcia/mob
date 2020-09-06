import discord
from discord.ext import commands, tasks
from itertools import cycle
from commandslist import *
from secret import Bot_token, bitly_token
import pandas as pd
# import bitlyshortener

#short = bitlyshortener.Shortener(tokens=bitly_token, vanitize=True)
Prefix = 'mack '
client = commands.Bot(command_prefix=Prefix)
status = cycle(['Estudando...', 'Navegando no Moodle', 'Descobrindo tarefas', 'Dominando o mundo', 'Reduzindo as suas faltas', 'Calculando as suas médias'])
PATH = r'C:\Users\lukep\Documents\Projects\Discord Bot\DiscordMackBot\csvfiles\events.csv'


@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))

#Discord live status that rotate from the list
@tasks.loop(seconds=300)
async def change_status():
    print("next status")
    await client.change_presence(activity=discord.Game(next(status)))

#Clear the previous line for x amout of times
@client.command()
async def clear(ctx, amount=3):
    print("clear command")
    await ctx.channel.purge(limit=amount)

#Command to get the assignments from the csv and send it embeded to the text chat
@client.command()
async def assignments(ctx):
    database = pd.read_csv(PATH, header=None )
    
    # urls = pd.DataFrame(database, columns=['deadline'])
    # print(urls, type(urls))
    for i in range(len(database)):# amount of rows of the csv
        fullname = database.iat[i,0]
        name = database.iat[i,1]
        description = database.iat[i,2]
        modulename = database.iat[i,3]
        deadline = database.iat[i,4] + ' às ' + database.iat[i,5]
        link = database.iat[i, 6]
        # url = urls[i]
        # print(link, url)
        # print(database)


        #Creating a style for the message 
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
