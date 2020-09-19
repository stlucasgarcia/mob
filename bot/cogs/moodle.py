import discord, asyncio
from moodleapi.security import Cryptography
from moodleapi.token import Token
from moodleapi.data.calendar import Calendar
from moodleapi.data.export import Export


from discord.ext import commands, tasks
from settings import *
from utilities import *
from utilities_moodle import *
import pandas as pd
from datetime import datetime

#list with commands/functionalities related to the Moodle API
class Moodle(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.GetData.start()

     
    # Command to get the assignments from the csv and send it embeded to the text chat    
    @commands.command()
    async def Get(self, ctx, option=""):
        isBool = True
        # Check if the bot has permission to send messages on the specified channel, used in most commands
        if ctx.channel.id in allowed_channels:
            option = option.lower()
            # Get path for what the user desires 
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
                isBool = False
            
            
            if isBool:
                amount = 0
                await ctx.message.add_reaction(next(positive_emojis_list))
                for i in range(len(database)):# amount of rows of the csv
                    amount += 1
                    assignmentsdata = data_dict(i, database)

                    #Styling the message for better user experience
                    if option == "assignments":
                        if i % 2 == 0: 
                            color = 0x480006
                        else:
                            color = 0x9f000c
                    elif option == "classes":
                        if i % 2 == 0: 
                            color = 0x29C8BA
                        else:
                            color = 0x155D56
                    elif option == "events":
                        if assignmentsdata["modulename"] == "Tarefa para entregar via Moodle":
                            if i % 2 == 0: 
                                color = 0x480006
                            else:
                                color = 0x9f000c
                        else:
                            if i % 2 == 0: 
                                color = 0x29C8BA
                            else:
                                color = 0x155D56

                    embed = check_command_style(assignmentsdata, str(amount),color)
                    await ctx.send(embed=embed)
                    await asyncio.sleep(1)

            embed = main_messages_style(f"=========There were a total of {amount} {option.capitalize()}=========")
            await asyncio.sleep(1)
            await ctx.send(embed=embed)

    #Command to check if the assignments were done at the Moodle website
    @commands.command()
    async def Check(self, ctx):
        # Reads the csv file to check if the hw was done
        tokens_data = pd.read_csv(PATH_TOKENS, header=None)
        userid = str(ctx.author.id)
        token = 0

        #Get user token from tokens.csv
        for i in range(len(tokens_data)):
            if str(userid) == str(tokens_data.iat[i,1]):
                token = tokens_data.iat[i,0]
                
        embed = main_messages_style("Checking your assignments...")
        await ctx.author.send(embed=embed)

        # Decrypt the token and get Calendar
        decrypted_token = Cryptography().decrypt_message(bytes(token, encoding='utf-8'))
        ca = Calendar(decrypted_token)
        data = ca.monthly()
        

        assign = ca.filter(value="assign", data=data)

        #Check if there's assigns
        if assign:
            export_assign = Export('assignments.csv')
            export_assign.to_csv(data=assign, addstyle=False)

            
            amount = 0

            database = pd.read_csv(PATH_ASSIGNMENTS, header=None)
            for i in range(len(database)):
                amount += 1
                assignmentsdata = data_dict(i, database)

                # Style embed message
                if i % 2 == 0: 
                    color = 0x480006
                else:
                    color = 0x9f000c

                embed = check_command_style(assignmentsdata, str(amount), color, 1)
                await ctx.author.send(embed=embed)
                await asyncio.sleep(1)        

            await ctx.message.add_reaction(next(positive_emojis_list))
        else:
            embed = check_command_style("There weren't any scheduled assignments")
            await asyncio.sleep(1)
            await self.client.get_channel(int(750313490455068722)).send(embed=embed)
            await ctx.message.add_reaction(next(negative_emojis_list))
        


    # Command to create or access your moodle API token    
    @commands.command()
    async def GetToken(self, ctx):
        await ctx.message.add_reaction(next(positive_emojis_list))
        tokens_data = pd.read_csv(PATH_TOKENS, header=None )

        userid = str(ctx.author.id)
        
        def check(ctx, m):
            return m.author == ctx.author

        isBool = True

        # Check if a token for that user already exists
        j = 0
        for i in range(len(tokens_data)):
            if userid in str(tokens_data.iat[i,1]):
                j = i
                isBool = False

        if isBool:
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

                # Call a function from moodleAPI to create a Token and save it encrypted on the file tokens.csv, it saves the discord author.id as well
                Token().create(username.content, password.content, userid)

                embed = main_messages_style("Your Token was created sucessfully")
                await ctx.author.send(embed=embed)

            else:
                embed = main_messages_style("Okay, use the **GetToken** command when you're ready to create one")
                await ctx.author.send(embed=embed)

        else:
            embed = main_messages_style("Your Moodle API Token is encripted and safe, to keep the institution and your data safe I will send the Token in your DM")
            await ctx.send(embed=embed)
            decrypted_token = Cryptography().decrypt_message(bytes(tokens_data.iat[j,0], encoding='utf-8'))
            embed = main_messages_style(f"Your decrypted Moodle API Token is, {decrypted_token}", "Note: You won't need to use it in this bot, your Token is already beeing used and is stores in our database")
            await ctx.author.send(embed=embed)

    # @commands.command()
    # async def RemindMe(self, ctx, message, day, month, time):
    #     if ctx.channel.id in allowed_channels:
    #         now = datetime.now()
    #         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    #         await ctx.send(dt_string)



    # Gets Moodle data through Moodle API and send it to the chat
    #Loops the GetData function. 
    @tasks.loop(hours=12)
    async def GetData(self):
        tokens_data = pd.read_csv(PATH_TOKENS, header=None )
        decrypted_token = Cryptography().decrypt_message(bytes(tokens_data.iat[0,0], encoding='utf-8'))
        database = pd.read_csv(PATH_EVENTS, header=None )

        embed = main_messages_style("=========Sending the twice-daily Moodle events update=========")
        await asyncio.sleep(1)
        await self.client.get_channel(int(750313490455068722)).send(embed=embed)

        # Get data from the Calendar and filter it
        ca = Calendar(decrypted_token)
        data = ca.monthly()
        assign = ca.filter(value="assign", data=data)
        liveclasses = ca.filter(value="bbb", data=data)

        # Check if there's assign, classes
        if assign:
            export_assign = Export('assignments.csv')
            export_assign.to_csv(data=assign, addstyle=False)

        if liveclasses:
            export_liveclasses = Export('liveclasses.csv')
            export_liveclasses.to_csv(data=liveclasses, addstyle=False)

        if data:
            export_events = Export('events.csv')
            export_events.to_csv(data=data, addstyle=False)

        if not data:
            embed = check_command_style("There weren't any event scheduled")
            await asyncio.sleep(1)
            await self.client.get_channel(int(750313490455068722)).send(embed=embed)
        amount = 0

        if data:
            for i in range(len(database)): #amount of rows of the csv
                amount += 1
                assignmentsdata = data_dict(i, database)

                #Styling the message to improve user experience
                if assignmentsdata["modulename"] == "Tarefa para entregar via Moodle":
                    if i % 2 == 0: 
                        color = 0x480006
                    else:
                        color = 0x9f000c
                else:
                    if i % 2 == 0: 
                        color = 0x29C8BA
                    else:
                        color = 0x155D56

                embed = check_command_style(assignmentsdata, str(amount),color)
                await asyncio.sleep(1)
                await self.client.get_channel(int(750313490455068722)).send(embed=embed)

            embed = main_messages_style(f"====There were a total of {amount} events, see you in 12 hours 😊 =====")
            await asyncio.sleep(1)
            await self.client.get_channel(int(750313490455068722)).send(embed=embed)

        

def setup(client):
    client.add_cog(Moodle(client))