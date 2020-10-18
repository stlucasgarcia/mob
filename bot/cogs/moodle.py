import asyncio

from moodleapi.security import Cryptography
from moodleapi.token import Token
from moodleapi.data.calendar import Calendar


from discord.ext import tasks
from discord.ext.commands import command, Cog, cooldown
from settings import allowed_channels, getData_Counter
from utilities import (
    main_messages_style,
    check_command_style,
    happy_faces,
    negative_emojis_list,
    books_list,
    positive_emojis_list,
)
from utilities_moodle import data_dict, moodle_color, loop_channel


# List with commands/functionalities related to the Moodle API
class Moodle(Cog):
    def __init__(self, client):
        self.client = client
        self.getData.start()

    @command(name="get", aliases=["Get", "GET"])
    async def get(self, ctx, option=""):
        """Get can show you all your Assignments, Events or Classes up to 2 weeks starting from the time you use the command. You must use Assignments, Events or Classes following the command"""

        isBool = True
        database = None
        guild_id = int(ctx.guild.id)

        # Check if the bot has permission to send messages on the specified channel, used in most commands
        if str(ctx.channel.id) in allowed_channels:
            option = option.lower()

            # Get data for what the user desires
            if option == "assignments":
                database = await self.client.pg_con.fetch(
                    "SELECT * FROM moodle_events WHERE subject_type = $1 AND guild_id = $2",
                    "Tarefa para entregar via Moodle",
                    guild_id,
                )
            elif option == "classes":
                database = await self.client.pg_con.fetch(
                    "SELECT * FROM moodle_events WHERE subject_type = $1 AND guild_id = $2",
                    "Aula ao vivo - BigBlueButton",
                    guild_id,
                )
            elif option == "events":
                database = await self.client.pg_con.fetch(
                    "SELECT * FROM moodle_events WHERE guild_id = $1", guild_id
                )

            else:
                embed = main_messages_style(
                    "Command **get** plus one of the following options will get assignments, classes or events from your Moodle calendar ",
                    "Option not available, you must use Assignments, Classes or Events ",
                    " 😕",
                )
                await ctx.message.add_reaction(next(negative_emojis_list))
                await ctx.send(embed=embed)
                isBool = False

            amount = 0  # Amount of data
            if isBool and database:
                embed = main_messages_style(
                    f"Checking {option.lower()} {next(books_list)} ..."
                )
                await ctx.send(embed=embed)

                await ctx.message.add_reaction(next(positive_emojis_list))

                for index in range(len(database)):
                    assignmentsdata = data_dict(database[index])

                    # Styling the message for better user experience
                    color = moodle_color(index, assignmentsdata)

                    amount += 1

                    embed = check_command_style(assignmentsdata, str(amount), color)[0]
                    await ctx.send(embed=embed)
                    await asyncio.sleep(0.5)

                if amount > 0:
                    embed = main_messages_style(
                        f"There was a total of {amount} {option} {next(books_list)}",
                        f"Note: I am only showing {option} of 14 days ahead ",
                    )
                    await ctx.send(embed=embed)

                elif amount > 1:
                    embed = main_messages_style(
                        f"There were a total of {amount} {option} {next(books_list)}",
                        f"Note: I am only showing {option} of 14 days ahead ",
                    )
                    await ctx.send(embed=embed)

            elif isBool:
                embed = main_messages_style(
                    f"There wasn't any scheduled {option} 😑 😮",
                    "Note: This is really weird, be careful 🤨 😶",
                )
                await ctx.send(embed=embed)

    # Command to check if the assignments were done at the Moodle website
    @command(name="check", aliases=["Check", "CHECK"])
    async def check(self, ctx):
        """Check command will send you a direct message with all your personal assignments status using the moodle API"""

        if str(ctx.channel.id) in allowed_channels:

            user_id = int(ctx.author.id)
            guild_id = int(ctx.guild.id)

            tokens_data = await self.client.pg_con.fetch(
                "SELECT token FROM moodle_profile WHERE discord_id = $1 AND guild_id = $2",
                user_id,
                guild_id,
            )
            token = tokens_data[0]["token"]

            params = {
                "db": "moodle_assign",
                "course": "CCP",
                "semester": "02",
                "class": "D",
                "discord_id": user_id,
                "guild_id": guild_id,
            }

            decrypted_token = Cryptography.decrypt_message(
                bytes(token, encoding="utf-8")
            )
            Calendar(decrypted_token).upcoming(True, params)

            database = await self.client.pg_con.fetch(
                "SELECT * FROM moodle_assign WHERE discord_id = $1 AND guild_id = $2",
                user_id,
                guild_id,
            )

            embed = main_messages_style(
                f"Checking your assignments {next(books_list)} ..."
            )
            await ctx.author.send(embed=embed)

            # Check if there's assigns
            if database:
                await ctx.message.add_reaction(next(positive_emojis_list))

                amount = 0
                done = 0

                for index in range(len(database)):

                    amount += 1

                    assignmentsdata = data_dict(database[index])

                    # Style embed message
                    color = moodle_color(index, assignmentsdata)

                    embed, done = check_command_style(
                        assignmentsdata, str(amount), color, 1, done
                    )
                    await ctx.author.send(embed=embed)
                    await asyncio.sleep(0.5)

                embed = main_messages_style(
                    f"You did {done} out of {amount} assignments {next(books_list)}",
                    "Note: I am only showing assignments of 14 days ahead",
                )
                await ctx.author.send(embed=embed)

            else:
                await ctx.message.add_reaction(next(negative_emojis_list))

                embed = main_messages_style(
                    "There weren't any scheduled events 😑😮",
                    "Note: This is really weird, be careful 🤨😶",
                )

                await asyncio.sleep(0.5)
                await ctx.author.send(embed=embed)

    # Command to create or access your moodle API token
    @command(
        name="getToken",
        aliases=[
            "GetToken",
            "gettoken",
            "GETTOKEN",
            "GETtoken",
            "getTOKEN",
            "GetT",
            "CreateToken",
            "createToken",
            "createtoken",
        ],
    )
    @cooldown(1, 20)
    async def getToken(self, ctx):
        """Generates your personal tooken at the moodle api and stores on the bots database, this command is the base for all moodle commands. The token is encrypted and stored in our database"""

        if str(ctx.channel.id) in allowed_channels:

            user_id = ctx.author.id
            guild_id = ctx.guild.id

            await ctx.message.add_reaction(next(positive_emojis_list))

            # Check if a token for that user already exists
            user_data = await self.client.pg_con.fetch(
                "SELECT token FROM moodle_profile WHERE discord_id = $1 AND guild_id = $2",
                user_id,
                guild_id,
            )

            def check(ctx, m):
                return m.author == ctx.author

            if not user_data:
                embed = main_messages_style(
                    "Apparently you don't have a Moodle API Token, do you want to create one? Yes/No",
                    "Your login and password won't be saved in the "
                    "system, it'll be used to create your Token and the Encrypted Token will be stored",
                )
                await ctx.author.send(embed=embed)

                answer = await self.client.wait_for("message")

                if answer.content.lower() == "yes":
                    embed = main_messages_style("Type and send your Moodle username")
                    await ctx.author.send(embed=embed)
                    await ctx.message.add_reaction(next(positive_emojis_list))

                    username = await self.client.wait_for("message")

                    embed = main_messages_style("Type and send your Moodle password")
                    await ctx.author.send(embed=embed)
                    await ctx.message.add_reaction(next(positive_emojis_list))

                    password = await self.client.wait_for("message")

                    # Call a function from moodleAPI to create a Token and save it encrypted on the file tokens.csv, it saves the discord author.id as well
                    params = {
                        "discord_id": int(user_id),
                        "tia": username.content,
                        "course": "CC",
                        "semester": "02",
                        "class": "D",
                        "guild_id": int(guild_id),
                    }

                    Token.create(
                        params, username=username.content, password=password.content
                    )

                    embed = main_messages_style("Your Token was created successfully")
                    await ctx.author.send(embed=embed)
                    await ctx.message.add_reaction(next(positive_emojis_list))

                else:
                    embed = main_messages_style(
                        "Okay, use the **GetToken** command when you're ready to create one"
                    )
                    await ctx.author.send(embed=embed)

            else:
                token = user_data[0]["token"]

                embed = main_messages_style(
                    "Your Moodle API Token is encripted and safe, to keep the institution and your data safe I will send the Token in your DM"
                )
                await ctx.send(embed=embed)

                decrypted_token = Cryptography().decrypt_message(
                    bytes(token, encoding="utf-8")
                )

                embed = main_messages_style(
                    f"Your decrypted Moodle API Token is, {decrypted_token}",
                    "Note: You won't need to use it in this bot, your Token is already being used and it's stored in our database",
                )
                await ctx.author.send(embed=embed)

    # Gets Moodle data through Moodle API and send it to the chat
    # Loops the GetData function.
    @tasks.loop(minutes=30)
    async def getData(self):
        CSmain = 169890240708870144

        params = {
            "db": "moodle_events",
            "course": "CCP",
            "semester": "02",
            "class": "D",
            "discord_id": CSmain,
            "guild_id": 748168924465594419,
        }

        try:
            tokens_data = await self.client.pg_con.fetch(
                "SELECT token FROM moodle_profile WHERE discord_id = $1", CSmain
            )

            token = tokens_data[0]["token"]

            decrypted_token = Cryptography.decrypt_message(
                bytes(token, encoding="utf-8")
            )

            # Get data from the moodle and filter it
            Calendar(decrypted_token).upcoming(False, params)

            # Check if there's events
            data = await self.client.pg_con.fetch(
                "SELECT * FROM moodle_events WHERE discord_id = $1 AND guild_id = $2",
                CSmain,
                748168924465594419,
            )

            # Counter for the amount of assignments/events
            amount = 0

            if data and getData_Counter[0] % 16 == 0:
                embed = main_messages_style(
                    f"Sending the twice-daily Moodle events update {next(books_list)} {next(happy_faces)}"
                )

                await asyncio.sleep(1)

                await self.client.get_channel(loop_channel).send(embed=embed)

                for index in range(len(data)):
                    amount += 1
                    assignmentsdata = data_dict(data[index])

                    # Styling the message to improve user experience
                    color = moodle_color(index, assignmentsdata)

                    embed = check_command_style(
                        assignmentsdata, str(amount), color, None
                    )[0]

                    await asyncio.sleep(0.5)
                    await self.client.get_channel(loop_channel).send(embed=embed)

                if amount > 0:
                    embed = main_messages_style(
                        f"There were a total of {amount} events {next(books_list)} see you in 8 hours {next(happy_faces)} ",
                        "Note: I am only showing events of 14 days ahead",
                    )

                    await asyncio.sleep(0.5)
                    await self.client.get_channel(loop_channel).send(embed=embed)

                else:
                    embed = main_messages_style(
                        "There weren't any scheduled events 😑😮",
                        "Note: This is really weird, be careful 🤨😶",
                    )

                    await asyncio.sleep(0.5)
                    await self.client.get_channel(loop_channel).send(embed=embed)

            getData_Counter[0] += 1

        except AttributeError:
            pass


def setup(client):
    client.add_cog(Moodle(client))
