import discord
from discord.ext import commands, tasks
from itertools import cycle
from commandslist import *
from secret import Bot_token, bitly_token
import pandas as pd
from os import path
import time
import asyncio

# import bitlyshortener

#short = bitlyshortener.Shortener(tokens=bitly_token, vanitize=True)
Prefix = 'mack '
client = commands.Bot(command_prefix=Prefix)
status = cycle(['Estudando...', 'Navegando no Moodle', 'Descobrindo tarefas', 'Dominando o mundo', 'Reduzindo as suas faltas', 'Calculando as suas médias'])

#PATH_EVENTS = path.join(path.abspath('bot')[:-3], path.abspath('csvfiles\events.csv'))
PATH_EVENTS = r'C:\\Users\\lukep\\Documents\\Projects\\Discord Bot\\DiscordMackBot\\csvfiles\\events.csv'
#PATH_ASSIGNMENTS = path.join(path.abspath('bot')[:-3], path.abspath('csvfiles\assignments.csv'))
#PATH_CLASSES = path.join(path.abspath('bot')[:-3], path.abspath('csvfiles\liveclasses.csv'))

allowed_channels = []
darkred = 0x9f000c
footer = embed.set_footer(text="Feito com ❤ por alunos do Mackenzie.")


@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))

#Discord live status that rotate from the list
@tasks.loop(seconds=300)
async def change_status():
    print("next status")
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def permissionschannel(ctx, choice=''):
    channel_id = ctx.channel.id
    choice = choice.lower()
    if choice != 'allow' and choice != 'disallow' and choice == '':
        embed=discord.Embed(description="Option not available, you must use Allow or Disallow", color=darkred)
        await ctx.channel.send(embed=embed)
        
    else:
        if choice == 'allow':
            if channel_id not in allowed_channels:
                allowed_channels.append(ctx.channel.id)
                print(ctx.channel.id)
                embed=discord.Embed(description=f"Now I will operate on #{client.get_channel(ctx.channel.id)}", color=darkred)
                await ctx.channel.send(embed=embed)
                # await ctx.channel.send(f"> Now I will operate on #{client.get_channel(allowed_channels[len(allowed_channels)-1])} !")
                print(allowed_channels)
            else:
                embed=discord.Embed(description="I already operate on this channel", color=darkred)
                await ctx.channel.send(embed=embed)

        elif choice == 'disallow':
            if channel_id in allowed_channels:
                allowed_channels.remove(ctx.channel.id)
                print(ctx.channel.id)
                embed=discord.Embed(description=f"I will no longer operate on #{client.get_channel(ctx.channel.id)}", color=darkred)
                await ctx.channel.send(embed=embed)
                # await ctx.channel.send(f"> Now I will operate on #{client.get_channel(allowed_channels[len(allowed_channels)-1])} !")
                print(allowed_channels)
            else:
                embed=discord.Embed(description="I already don't have permission to operate on this channel", color=darkred)
                await ctx.channel.send(embed=embed)
    
        

#Clear the previous line for x amout of times
@client.command()
async def clear(ctx, amount=3):
    if ctx.channel.id in allowed_channels:
        await ctx.channel.purge(limit=amount)
    print("clear command")

#Command to get the assignments from the csv and send it embeded to the text chat
@client.command()
async def assignments(ctx):
    database = pd.read_csv(PATH_EVENTS, header=None ) # This should equals PATH for assignments.csv
    
    # urls = pd.DataFrame(database, columns=['deadline'])
    # print(urls, type(urls))
    if ctx.channel.id in allowed_channels:
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
            embed=discord.Embed(title=modulename, color=darkred)
            embed.set_thumbnail(url="https://logodownload.org/wp-content/uploads/2017/09/mackenzie-logo-3.png")
            embed.add_field(name="Matéria", value=fullname, inline=True)
            embed.add_field(name="Nome da tarefa", value=name, inline=True)
            embed.add_field(name="Descrição", value=description, inline=False)
            embed.add_field(name="Tipo de tarefa", value=modulename, inline=True)
            embed.add_field(name="Data de entrega", value=deadline, inline=True)
            embed.add_field(name="Link", value=link, inline=False)
            embed.set_footer(text="Feito com ❤ por alunos do Mackenzie.")

            await ctx.channel.send(embed=embed)
            await asyncio.sleep(2)


client.run(Bot_token)
