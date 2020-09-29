import discord, asyncio
from moodleapi.security import Cryptography
from moodleapi.token import Token
from moodleapi.data.calendar import Calendar
from moodleapi.data.export import Export


from discord.ext import tasks
from discord.ext.commands import command, Cog, has_permissions
from settings import *
from utilities import *
from utilities_moodle import *
import pandas as pd
from datetime import datetime

class Admin(Cog):
    def __init__(self, client):
        self.client = client

     


        

def setup(client):
    client.add_cog(Admin(client))