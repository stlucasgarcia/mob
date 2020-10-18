import discord
from discord.ext.commands import Cog, command, has_permissions
from settings import allowed_channels
from utilities import positive_emojis_list


class Setup(Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Setup(client))