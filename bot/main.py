import discord, os

from discord.ext import commands, tasks
from itertools import cycle

from secret import Bot_token, bitly_token

#Create the bot prefix
Prefix = "mack "
client = commands.Bot(command_prefix=Prefix)
status = cycle(["Estudando...", "Navegando no Moodle", "Descobrindo tarefas", "Dominando o mundo", "Reduzindo as suas faltas", "Calculando as suas médias"])


#Load and get/initialize all the files .py(cogs) in the folder cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension((f"cogs.{filename[:-3]}"))


#Discord live status that rotate from the list
@tasks.loop(seconds=600)
async def change_status():
    print("next status")
    await client.change_presence(activity=discord.Game(next(status)))


client.run(Bot_token)