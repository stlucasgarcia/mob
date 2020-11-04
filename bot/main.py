import os
import asyncpg
import pyshorteners

from discord import Intents
from discord.ext import commands

from utilities import main_messages_style, positive_emojis_list
from secret1 import DB_Username, DB_Password, Bot_token, bitly_token


async def get_prefix(client, ctx) -> str:
    try:
        prefix = await client.pg_con.fetch(
            "SELECT prefix FROM bot_servers WHERE guild_id = $1", ctx.guild.id
        )
        prefix = prefix[0]["prefix"]
        return prefix

    except AttributeError or TypeError:
        return "--"


intents = Intents.all()
client = commands.Bot(command_prefix=get_prefix, help_command=None, intents=intents)

# Creates a connection with the Discord Database
async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(
        database="DiscordDB", user=DB_Username, password=DB_Password
    )


# Load and get/initialize all the files .py(cogs) in the folder cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.message.add_reaction(next(positive_emojis_list))

    print(f"{extension.capitalize()} successfully re-loaded")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = main_messages_style(
            "Invalid command",
            f"Type {await get_prefix(client, ctx)}help to see the available commands",
        )
        await ctx.send(embed=embed)


@client.event
async def on_guild_join(guild):
    await client.pg_con.execute(
        "INSERT INTO bot_servers (guild_id, guild_name, prefix, moodle_url) VALUES ($1, $2, $3, $4)",
        int(guild.id),
        str(guild.name),
        "--",
        None,
    )


@client.event
async def on_guild_remove(guild):
    await client.pg_con.execute(
        "DELETE FROM {bot_servers, bot_data, moodle_events, moodle_groups, moodle_professors, moodle_professors} WHERE guild_id = $1",
        int(guild.id),
    )

    await client.pg_con.execute(
        "DELETE FROM bot_roles WHERE guild_id = $1",
        str(guild.id),
    )


client.loop.run_until_complete(create_db_pool())

client.run(Bot_token)
