import discord

from discord.ext import commands, tasks
from settings import *
from style import *


class General2(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def GetToken(self, ctx):
        embed = main_messages_style("Your Moodle API Token is encripted and safe, to keep the school/university and your data safe I will send the Token in your DM")
        await ctx.send(embed=embed)

        embed = main_messages_style("Type and send your Moodle API Token here")
        await ctx.author.send(embed=embed)
        # on_message()

    # @commands.Cog.listener()
    # async def on_message(self, ctx):
    #     msg = await self.client.wait_for('message', check=check)

    #     # content = ctx.content
        # print(content)
        # if message.startswith(" "):
        #     await ctx.author.send(message)




def setup(client):
    client.add_cog(General2(client))