import os
import asyncpg

from discord.ext import commands

from utilities import main_messages_style, positive_emojis_list

from secret1 import DB_Username, DB_Password, Bot_token


async def get_preffix(client, ctx):
    preffix = await client.pg_con.fetch(
        "SELECT preffix FROM bot_servers WHERE guild_id = $1", ctx.guild.id
    )
    preffix = preffix[0]["preffix"]
    return preffix


client = commands.Bot(command_prefix=get_preffix, help_command=None)

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
            "Invalid command", f"Type {get_preffix}help to see the available commands"
        )
        await ctx.send(embed=embed)


@client.event
async def on_guild_join(guild):
    await client.pg_con.execute(
        "INSERT INTO bot_servers (guild_id, guild_name, preffix) VALUES ($1, $2, $3)",
        int(guild.id),
        str(guild.name),
        "mack ",
    )


@client.event
async def on_guild_remove(guild):
    await client.pg_con.execute(
        "DELETE FROM bot_servers WHERE guild_id = $1",
        int(guild.id),
    )

    await client.pg_con.execute(
        "DELETE FROM bot_data WHERE guild_id = $1",
        int(guild.id),
    )

    await client.pg_con.execute(
        "DELETE FROM bot_roles WHERE guild_id = $1",
        str(guild.id),
    )


client.loop.run_until_complete(create_db_pool())

client.run(Bot_token)