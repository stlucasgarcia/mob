import youtube_dl, discord

from discord.ext.commands import Cog, command
from discord.voice_client import VoiceClient
from discord.utils import get
from utilities import main_messages_style, positive_emojis_list
from settings import allowed_channels

class Music(Cog):
    def __init__(self, client):
        self.client = client


    @command(name="Join", aliases=["JOIN", "join"])
    async def join(self, ctx):
        """Join command is used to make the bot join to the voice chat which you're in"""
        if str(ctx.channel.id) in allowed_channels:
            await ctx.message.add_reaction(next(positive_emojis_list))

            channel = ctx.message.author.voice.channel

            if not channel:
                embed = main_messages_style(f"You {ctx.author.mention} are not connected to a voice channel")
                await ctx.send(embed=embed)
                return

            voice = get(self.client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()
                voice = await channel.connect()

                embed = main_messages_style(f"The bot moved to `{channel}`")
                await ctx.send(embed=embed)

            else:
                voice = await channel.connect()

                embed = main_messages_style(f"The bot is now connected to `{channel}`")
                await ctx.send(embed=embed)

    

    @command(name="Leave", aliases=["LEAVE", "leave"])
    async def leave(self, ctx):
        """Leave command is used to make the bot disconnect from any voice chat"""
        if str(ctx.channel.id) in allowed_channels:
            await ctx.message.add_reaction(next(positive_emojis_list))

            channel = ctx.message.author.voice.channel

            voice = get(self.client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()

            else:
                embed = main_messages_style("The bot is not connected to any voice channel")
                await ctx.send(embed=embed)


    @command(name="Play", aliases=["play", "PLAY"])
    async def play(self, ctx, url: str):
        """Makes the bot play a song by link"""


def setup(client):
    client.add_cog(Music(client))