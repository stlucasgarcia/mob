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
                decrypted_token = Cryptography().decrypt_message(bytes(tokens_data.iat[i,0], encoding='utf-8'))
                embed = main_messages_style(f"Your decrypted Moodle API Token is, {decrypted_token}", "Note: You won't need to use it anywhere in this bot")
                await ctx.author.send(embed=embed)

            else:
                embed = main_messages_style("Apparently you don't have a Moodle API Token, do you want to create one? Yes/No")
                await ctx.author.send(embed=embed)
                answer = await self.client.wait_for('message')

                if answer.content.lower() == "yes":

                    embed = main_messages_style("Type and send your Moodle username")
                    await ctx.author.send(embed=embed)
                    username = await self.client.wait_for('message')

                    embed = main_messages_style("Type and send your Moodle passowrd")
                    await ctx.author.send(embed=embed)
                    password = await self.client.wait_for('message')

                    Token().create(username, password, userid)


                else:
                    embed = main_messages_style("Okay, use the **GetToken** command when you're ready to create one")
                    await ctx.author.send(embed=embed)

def setup(client):
    client.add_cog(General2(client))