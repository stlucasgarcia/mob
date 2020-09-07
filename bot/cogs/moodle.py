import discord, asyncio
import pandas as pd

from discord.ext import commands
from settings import *
from style import *

#list with commands/functionalities related to the Moodle API
class Moodle(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command to get the assignments from the csv and send it embeded to the text chat    
    @commands.command()
    async def check(self, ctx, option):        
        # urls = pd.DataFrame(database, columns=["deadline"])
        # print(urls, type(urls))
        if ctx.channel.id in allowed_channels:

            if option == "assignments":
                database = pd.read_csv(PATH_ASSIGNMENTS, header=None )
            elif option == "classes":
                database = pd.read_csv(PATH_CLASSES, header=None )
            elif option == "events":
                database = pd.read_csv(PATH_EVENTS, header=None )
            else:
                embed = main_messages_style("Command **check** plus one of the following options will get assignments, classes or events from your Moodle calendar ",
                "Option not available, you must use Assignments, Classes or Events ", " 😕")
                await ctx.message.add_reaction(next(negative_emojis_list))
                await ctx.send(embed=embed)                
                database = None

            if database:
                for i in range(len(database)):# amount of rows of the csv
                    assignmentsdata = { 
                    "fullname" : database.iat[i,0],
                    "name" : database.iat[i,1],
                    "description" : database.iat[i,2],
                    "modulename" : database.iat[i,3],
                    "deadline" : database.iat[i,4] + " às " + database.iat[i,5],
                    "link" : database.iat[i, 6]
                    # "author" : database.iat[i, 7]
                    }
                    # url = urls[i]
                    # print(link, url)
                    # print(database)
                    
                    #Styling the message 
                    embed = check_command_style(assignmentsdata)
                    await ctx.message.add_reaction(next(positive_emojis_list))
                    await ctx.send(embed=embed)
                    await asyncio.sleep(2)

            else:
                pass


def setup(client):
    client.add_cog(Moodle(client))