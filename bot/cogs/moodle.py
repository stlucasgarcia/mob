import discord, asyncio
from moodleapi.security import Cryptography
from moodleapi.token import Token
from moodleapi.data.calendar import Calendar
from moodleapi.data.export import Export


from discord.ext import tasks
from discord.ext.commands import command, Cog, has_permissions
from settings import PATH_ASSIGNMENTS, PATH_CLASSES, PATH_EVENTS, PATH_TOKENS, allowed_channels
from utilities import main_messages_style, check_command_style, happy_faces, negative_emojis_list, books_list, positive_emojis_list 
from utilities_moodle import data_dict, moodle_color, loop_channel
import pandas as pd
from datetime import datetime

#list with commands/functionalities related to the Moodle API
class Moodle(Cog):

    def __init__(self, client):
        self.client = client
        self.getData.start()
        

    # Command to get the assignments from the csv and send it embeded to the text chat    
    @command(name='get', aliases=['Get', 'GET'])
    async def get(self, ctx, option=""):
        '''Get can show you all your Assignments, Events or Classes' up to 2 weeks'''
        channel_id = str(ctx.channel.id)
        isBool = True

        # Check if the bot has permission to send messages on the specified channel, used in most commands

        if channel_id in allowed_channels:
            option = option.lower()
            # Get path for what the user desires 
            if option == "assignments":
                database = pd.read_csv(PATH_ASSIGNMENTS, header=None )
            elif option == "classes":
                database = pd.read_csv(PATH_CLASSES, header=None )
            elif option == "events":
                database = pd.read_csv(PATH_EVENTS, header=None )
            else:

                embed = main_messages_style("Command **get** plus one of the following options will get assignments, classes or events from your Moodle calendar ",
                "Option not available, you must use Assignments, Classes or Events ", " 😕")
                await ctx.message.add_reaction(next(negative_emojis_list))
                await ctx.send(embed=embed)   
                isBool = False
            

            if isBool:
                embed = main_messages_style(f"Checking {option.lower()} {next(books_list)} ...")
                await ctx.send(embed=embed)


                amount = 0 #Amount of data
                await ctx.message.add_reaction(next(positive_emojis_list))
                for index in range(len(database)):# amount of rows of the csv
                    assignmentsdata = data_dict(index, database)

                    #Styling the message for better user experience
                    color = moodle_color(index, assignmentsdata)

                    amount += 1

                    embed = check_command_style(assignmentsdata, str(amount), color)[0]
                    await ctx.send(embed=embed)
                    await asyncio.sleep(1)


            embed = main_messages_style(f"There were a total of {amount} {option.capitalize()} {next(books_list)}", f"Note: I am only showing {option.capitalize()} of 14 days ahead ")
            await asyncio.sleep(0.5)
            await ctx.send(embed=embed)


    #Command to check if the assignments were done at the Moodle website
    @command(name='check', aliases=['Check', 'CHECK'])
    
    async def check(self, ctx):
        '''Check will send you a direct message with all your personal assignments status'''
        channel_id = str(ctx.channel.id)

        if channel_id in allowed_channels:

            # Reads the csv file to check if the hw was done
            tokens_data = pd.read_csv(PATH_TOKENS, header=None)
            userid = str(ctx.author.id)
            token = 0

            #Get user token from tokens.csv
            for i in range(len(tokens_data)):
                if str(userid) == str(tokens_data.iat[i,1]):
                    token = tokens_data.iat[i,0]
                    
            embed = main_messages_style(f"Checking your assignments {next(books_list)} ...")
            await ctx.author.send(embed=embed)

            # Decrypt the token and get Calendar
            decrypted_token = Cryptography().decrypt_message(bytes(token, encoding='utf-8'))
            ca = Calendar(decrypted_token)
            data = ca.monthly()
            

            assign = ca.filter(value="assign", data=data)

            #Check if there's assigns
            if assign:
                await ctx.message.add_reaction(next(positive_emojis_list))
                export_assign = Export('assignments.csv')
                export_assign.to_csv(data=assign, addstyle=False)

                
                amount = 0
                done = 0
                database = pd.read_csv(PATH_ASSIGNMENTS, header=None)

                for index in range(len(database)):
                    amount += 1
                    assignmentsdata = data_dict(index, database)

                    # Style embed message
                    color = moodle_color(index, assignmentsdata)


                    embed, done = check_command_style(assignmentsdata, str(amount), color, 1, done)
                    await ctx.author.send(embed=embed)
                    await asyncio.sleep(1)        


                embed = main_messages_style(f"You did {done} out of {amount} assignments {next(books_list)}", "Note: I am only showing assignments of 14 days ahead")
                await ctx.author.send(embed=embed)

            else:
                
                await ctx.message.add_reaction(next(negative_emojis_list))
                embed = check_command_style("There weren't any scheduled assignments 😑😮")
                await asyncio.sleep(0.5)
                await ctx.author.send(embed=embed)
        

    # Command to create or access your moodle API token    
    @command(name='getToken', aliases=['GetToken', 'gettoken', 'GETTOKEN', 'GETtoken', 'getTOKEN', 'GetT'])
    async def getToken(self, ctx):
        '''Helps you to get your Moodle Token for Check command'''
        channel_id = str(ctx.channel.id)

        if channel_id in allowed_channels:

            await ctx.message.add_reaction(next(positive_emojis_list))
            tokens_data = pd.read_csv(PATH_TOKENS, header=None )

            userid = str(ctx.author.id)
            
            def check(ctx, m):
                return m.author == ctx.author

            isBool = True

            # Check if a token for that user already exists
            j = 0
            for index in range(len(tokens_data)):
                if userid in str(tokens_data.iat[index,1]):
                    j = index
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
                embed = main_messages_style(f"Your decrypted Moodle API Token is, {decrypted_token}", "Note: You won't need to use it in this bot, your Token is already being used and it's stored in our database")
                await ctx.author.send(embed=embed)


    # Gets Moodle data through Moodle API and send it to the chat
    # Loops the GetData function. 
    @tasks.loop(hours=12)
    async def getData(self):
        CSmain = 0

        # params = {
        #     'discord_id': 169890240708870144,
        #     'tia' : "32023006",
        #     'course' : 'CC',
        #     'semester' : '02',
        #     'class' : 'D',
        #     'guild_id' : 748168924465594419,
        # }

        #Token().create(params, username="32023006", password='a')


        # tokens_data = await self.client.pg_con.fetch("SELECT token FROM moodle_profile WHERE discord_id = $1", 169890240708870144)
        # print(tokens_data)
        # print(tokens_data[0][0])
        tokens_data = pd.read_csv(PATH_TOKENS, header=None )
        decrypted_token = Cryptography().decrypt_message(bytes(tokens_data.iat[CSmain,0], encoding='utf-8'))


        # loop_channel = int(750313490455068722)
        embed = main_messages_style(f"Sending the twice-daily Moodle events update {next(books_list)} {next(happy_faces)}")
        await asyncio.sleep(1)
        await self.client.get_channel(loop_channel).send(embed=embed)

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
            embed = check_command_style("There weren't any scheduled events 😑😮")
            await asyncio.sleep(1)
            await self.client.get_channel(loop_channel).send(embed=embed)

        # Counter for the amount of assignments/events    
        amount = 0

        if data:
            database = pd.read_csv(PATH_EVENTS, header=None )
            for index in range(len(database)): #amount of rows of the csv
                amount += 1
                assignmentsdata = data_dict(index, database)

                #Styling the message to improve user experience
                color = moodle_color(index, assignmentsdata)


                embed = check_command_style(assignmentsdata, str(amount), color, None)[0]
                await asyncio.sleep(1)
                await self.client.get_channel(loop_channel).send(embed=embed)

            embed = main_messages_style(f"There were a total of {amount} events {next(books_list)} see you in 12 hours {next(happy_faces)} ", "Note: I am only showing events of 14 days ahead")
            await asyncio.sleep(0.5)
            await self.client.get_channel(loop_channel).send(embed=embed)


        
def setup(client):
    client.add_cog(Moodle(client))