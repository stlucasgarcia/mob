import discord, os, asyncpg

from discord.ext import commands

from secret import Bot_token, bitly_token, DataBase_Username, DataBase_Password

from utilities import main_messages_style

#Create the bot prefix
Prefix = "mack "
client = commands.Bot(command_prefix=Prefix, help_command=None)


async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(database="DiscordDB", user=DataBase_Username, password=DataBase_Password)


#Load and get/initialize all the files .py(cogs) in the folder cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'{extension.capitalize()} successfully re-loaded')


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = main_messages_style("Comando inválido", "Digite mack help para ver os comandos disponiveis")
        await ctx.send(embed=embed)
        
client.loop.run_until_complete(create_db_pool())
client.run(Bot_token)