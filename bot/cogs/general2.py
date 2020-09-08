import discord
from moodleapi.security import Cryptography
from moodleapi.token import Token

from discord.ext import commands, tasks
from settings import *
from style import *
import pandas as pd

class General2(commands.Cog):
    def __init__(self, client):
        self.client = client
        

def setup(client):
    client.add_cog(General2(client))