import discord
from discord.ext import commands, tasks
from itertools import cycle
from commandslist import *
from secret import Bot_token, bitly_token
import pandas as pd
from style import *
from os import path
import time
import asyncio

# import bitlyshortener

#short = bitlyshortener.Shortener(tokens=bitly_token, vanitize=True)
Prefix = "mack "
client = commands.Bot(command_prefix=Prefix)
status = cycle(["Estudando...", "Navegando no Moodle", "Descobrindo tarefas", "Dominando o mundo", "Reduzindo as suas faltas", "Calculando as suas médias"])

#PATH_EVENTS = path.join(path.abspath("bot")[:-3], path.abspath("csvfiles\events.csv"))
PATH_EVENTS = r"C:\\Users\\lukep\\Documents\\Projects\\Discord Bot\\DiscordMackBot\\csvfiles\\events.csv"
#PATH_ASSIGNMENTS = path.join(path.abspath("bot")[:-3], path.abspath("csvfiles\assignments.csv"))
#PATH_CLASSES = path.join(path.abspath("bot")[:-3], path.abspath("csvfiles\liveclasses.csv"))
darkred = 0x9f000c
allowed_channels = [750313490455068722]



@client.event
async def on_ready():
    change_status.start()
    print("We have logged in as {0.user}".format(client))

#Discord live status that rotate from the list
@tasks.loop(seconds=300)
async def change_status():
    print("next status")
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def permissionschannel(ctx, choice=""):
    channel_id = ctx.channel.id
    choice = choice.lower()
    if choice != "allow" and choice != "disallow" and choice == "":
        embed = main_messages_style("Option not available, you must use Allow or Disallow", "😕")
        await ctx.channel.send(embed=embed)

    else:
        if choice == "allow":
            if channel_id not in allowed_channels:
                allowed_channels.append(ctx.channel.id)
                embed = main_messages_style(f"Now I will operate on #{client.get_channel(ctx.channel.id)}")
                await ctx.channel.send(embed=embed)
            else:
                embed =main_messages_style("I already operate on this channel")
                await ctx.channel.send(embed=embed)

        elif choice == "disallow":
            if channel_id in allowed_channels:
                allowed_channels.remove(ctx.channel.id)
                embed = main_messages_style(f"I will no longer operate on #{client.get_channel(ctx.channel.id)}")
                await ctx.channel.send(embed=embed)
            else:
                embed = main_messages_style("I already don't have permission to operate on this channel")
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
    
    # urls = pd.DataFrame(database, columns=["deadline"])
    # print(urls, type(urls))
    if ctx.channel.id in allowed_channels:
        for i in range(len(database)):# amount of rows of the csv
            assignmentsdata = { 
            "fullname" : database.iat[i,0],
            "name" : database.iat[i,1],
            "description" : database.iat[i,2],
            "modulename" : database.iat[i,3],
            "deadline" : database.iat[i,4] + " às " + database.iat[i,5],
            "link" : database.iat[i, 6]
            # author = database.iat[i, 7]
            }
            # url = urls[i]
            # print(link, url)
            # print(database)
            
            #Styling the message 
            embed = assignments_style(assignmentsdata)
            await ctx.channel.send(embed=embed)
            await asyncio.sleep(2)


client.run(Bot_token)
