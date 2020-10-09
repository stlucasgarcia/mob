import youtube_dl, discord, os

from discord.ext.commands import Cog, command
from discord.voice_client import VoiceClient
from discord.utils import get
from utilities import main_messages_style
from settings import allowed_channels

class Music(Cog):
    def __init__(self, client):
        self.client = client


    @command(name="Join", aliases=["JOIN", "join", "j"])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()



def setup(client):
    client.add_cog(Music(client))