import discord
from moodleapi.token import Token
from moodleapi.security import Cryptography

from discord.ext import commands, tasks
from settings import *
from style import *
import pandas as pd

class General2(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def GetToken(self, ctx):
        tokens_data = pd.read_csv(PATH_TOKENS, header=None )
        userid = str(ctx.author.id)

        def check(ctx, m):
            return m.author == ctx.author

        for i in range(len(tokens_data)):
            if userid in str(tokens_data.iat[i,1]):
                embed = main_messages_style("Your Moodle API Token is encripted and safe, to keep the institution and your data safe I will send the Token in your DM")
                await ctx.send(embed=embed)
                embed = main_messages_style(f"Your decrypted Moodle API Token is, {decrypted_token}", "Note: You won't need to use it anywhere in this bot")

            else:
                embed = main_messages_style("Apparently you don't have a Moodle API Token, do you want to create one? Yes/No")
                await ctx.author.send(embed=embed)
                answer = await self.client.wait_for('message')

                if answer.content.lower() == "yes" or answer.content.lower() == "y":

                    embed = main_messages_style("Type and send your Moodle username")
                    await ctx.author.send(embed=embed)
                    username = await self.client.wait_for('message')

                    embed = main_messages_style("Type and send your Moodle passowrd")
                    await ctx.author.send(embed=embed)
                    passowrd = await self.client.wait_for('message')

                else:
                    embed = main_messages_style("Okay, use the **GetToken** command when you're ready to create one")
                    await ctx.author.send(embed=embed)

def setup(client):
    client.add_cog(General2(client))