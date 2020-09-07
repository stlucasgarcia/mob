import discord, os

from discord.ext import commands

from secret import Bot_token, bitly_token

#Create the bot prefix
Prefix = "mack "
client = commands.Bot(command_prefix=Prefix)

#Load and get/initialize all the files .py(cogs) in the folder cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(Bot_token)