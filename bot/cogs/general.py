import discord
import time

from typing import Optional

from discord.ext import tasks
from discord.ext.commands import command, Cog

from utilities import (
    main_messages_style,
    positive_emojis_list,
    status_list,
)


# General use bot commands
class General(Cog):
    def __init__(self, client):
        self.client = client

    # Print in the console when the bot starts to run (if everything is working perfectly)
    @Cog.listener()
    async def on_ready(self):
        print("Ready!")
        print("Logged in as ", self.client.user)
        print("ID:", self.client.user.id)

        self.change_status.start()

    # Discord live status that rotate from the list each 600 seconds
    @tasks.loop(seconds=600)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status_list)))

    # Delete the previous line for x amount of times
    @command(
        name="clear",
        aliases=["purge", "Clear", "CLEAR", "Delete", "delete", "del", "DELETE"],
    )
    async def clear(self, ctx, amount: Optional[int] = 2):
        """Delete previous chat messages by the amount given, """

        await ctx.channel.purge(limit=amount)

        embed = main_messages_style(f"The bot deleted {amount} messages successfully")
        await ctx.send(embed=embed, delete_after=2)

    # Print an embed message on the chat
    @command(
        name="printm", aliases=["Print", "PrintM", "print", "Printmessage", "PRINT"]
    )
    async def printm(self, ctx, name, message, emote=""):
        """Print an embed message"""

        embed = main_messages_style(name, message, emote)
        await ctx.send(embed=embed)

        await ctx.message.add_reaction(next(positive_emojis_list))

    # TODO Fix printm

    # Check latency/ping
    @Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.client.user:
            return

        if ctx.content.startswith("ping"):
            before = time.monotonic()

            embed = main_messages_style("Checking ping...")
            await ctx.channel.send(embed=embed)

            ping = (time.monotonic() - before) * 1000
            await ctx.channel.purge(limit=1)

            embed = main_messages_style(f"Pong!  🏓  `{int(ping)}ms`")
            await ctx.channel.send(embed=embed)

            print(f"Ping {int(ping)}ms")


def setup(client):
    client.add_cog(General(client))
