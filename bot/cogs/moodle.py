import discord
from moodleapi.security import Cryptography
from moodleapi.token import Token

from discord.ext import commands, tasks
from settings import *
from style import *
import pandas as pd

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

    # Command to create or access your moodle API        
    @commands.command()
    async def GetToken(self, ctx):
        await ctx.message.add_reaction(next(positive_emojis_list))
        tokens_data = pd.read_csv(PATH_TOKENS, header=None )
        userid = str(ctx.author.id)
        
        def check(ctx, m):
            return m.author == ctx.author

        flag = False

        j = 0
        for i in range(len(tokens_data)):
            if userid in str(tokens_data.iat[i,1]):
                j = i
                flag = True

        if not flag:
            embed = main_messages_style("Apparently you don't have a Moodle API Token, do you want to create one? Yes/No", "Your login and password won't be saved in the "
            "system, it'll be used to create your Token and the Crypted Token will be stored")
            await ctx.author.send(embed=embed)

            answer = await self.client.wait_for('message')

            if answer.content.lower() == "yes":
                embed = main_messages_style("Type and send your Moodle username")
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction(next(positive_emojis_list))

                username = await self.client.wait_for('message')
                

                embed = main_messages_style("Type and send your Moodle password")
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction(next(positive_emojis_list))
                password = await self.client.wait_for('message')
                # Call your
                Token().create(username.content, password.content, userid)

                embed = main_messages_style("Your Token was created sucessfully")
                await ctx.author.send(embed=embed)

            else:
                embed = main_messages_style("Okay, use the **GetToken** command when you're ready to create one")
                await ctx.author.send(embed=embed)

        if flag:
            embed = main_messages_style("Your Moodle API Token is encripted and safe, to keep the institution and your data safe I will send the Token in your DM")
            await ctx.send(embed=embed)
            decrypted_token = Cryptography().decrypt_message(bytes(tokens_data.iat[j,0], encoding='utf-8'))
            embed = main_messages_style(f"Your decrypted Moodle API Token is, {decrypted_token}", "Note: You won't need to use it anywhere in this bot")
            await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(Moodle(client))