import asyncio

from moodleapi.security import Cryptography
from moodleapi.token import Token
from moodleapi.data.calendar import Calendar

from discord import Embed
from discord.ext import tasks
from discord.ext.commands import command, Cog, cooldown
from settings import getData_Counter

from utilities import (
    main_messages_style,
    happy_faces,
    negative_emojis_list,
    books_list,
    positive_emojis_list,
    footer,
    defaultcolor,
    emojis_list,
)
from utilities_moodle import data_dict, moodle_color, check_command_style


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
        option = option.lower()

        assignments_options = ["assignments", "assign", "hw", "homework", "projects"]
        classes_options = [
            "classes",
            "live_classes",
            "bbb",
            "bigbluebutton",
            "big_blue_botton",
            "lecture",
            "lesson",
        ]
        events_options = ["events", "all", "everything", "calendar"]

        # Get data for what the user desires
        if option in assignments_options:
            database = await self.client.pg_con.fetch(
                "SELECT * FROM moodle_events WHERE subject_type = $1 AND guild_id = $2",
                "Tarefa para entregar via Moodle",
                guild_id,
            )
            option = "assignments"
        elif option in classes_options:
            database = await self.client.pg_con.fetch(
                "SELECT * FROM moodle_events WHERE subject_type = $1 AND guild_id = $2",
                "Aula ao vivo - BigBlueButton",
                guild_id,
            )
            option = "classes"
        elif option in events_options:
            database = await self.client.pg_con.fetch(
                "SELECT * FROM moodle_events WHERE guild_id = $1", guild_id
            )
            option = "events"

        else:
            embed = main_messages_style(
                "Command **get** plus one of the following options will get assignments, classes or events from your Moodle calendar ",
                "Option not available, you must use Assignments, Classes or Events ",
                " 😕",
            )
            await ctx.message.add_reaction(next(negative_emojis_list))
            await ctx.send(embed=embed)
            isBool = False

        if isBool and database:
            amount = len(database)  # Amount of data

            embed = main_messages_style(
                f"Checking {option.lower()} {next(books_list)} ..."
            )
            await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))

            for index in range(amount):
                assignmentsdata = data_dict(database[index])

                # Styling the message for better user experience
                color = moodle_color(index, assignmentsdata)

                embed = check_command_style(
                    assignmentsdata, str(index + 1), color
                )[0]
                await ctx.send(embed=embed)
                await asyncio.sleep(0.3)

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

        elif isBool and not database:
            embed = main_messages_style(
                f"There wasn't any scheduled {option} 😑 😮",
                "Note: This is really weird, be careful 🤨 😶",
            )
            await ctx.send(embed=embed)

    # Command to check if the assignments were done at the Moodle website
    @command(name="check", aliases=["Check", "CHECK", "Verify", "verify"])
    async def check(self, ctx):
        """Check command will send you a direct message with all your personal assignments status using the moodle API"""

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

        embed = main_messages_style(f"Checking your assignments {next(books_list)} ...")
        await ctx.author.send(embed=embed)

        decrypted_token = Cryptography.decrypt_message(bytes(token, encoding="utf-8"))
        Calendar(decrypted_token).upcoming(True, params)

        database = await self.client.pg_con.fetch(
            "SELECT * FROM moodle_assign WHERE discord_id = $1 AND guild_id = $2",
            user_id,
            guild_id,
        )

        # Check if there's assigns
        if database:
            await ctx.message.add_reaction(next(positive_emojis_list))

            amount = len(database)
            done = 0

            for index in range(amount):

                assignmentsdata = data_dict(database[index])

                # Style embed message
                color = moodle_color(index, assignmentsdata)

                embed, done = check_command_style(
                    assignmentsdata, str(index + 1), color, 1, done
                )

                await ctx.author.send(embed=embed)
                await asyncio.sleep(0.3)

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

            await asyncio.sleep(0.3)
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

        user_id = ctx.author.id
        guild_id = ctx.guild.id

        await ctx.message.add_reaction(next(positive_emojis_list))

        # Check if a token for that user already exists
        user_data = await self.client.pg_con.fetch(
            "SELECT token FROM moodle_profile WHERE discord_id = $1 AND guild_id = $2",
            user_id,
            guild_id,
        )

        def check(message):
            return message.author == ctx.author

        if not user_data:
            embed = main_messages_style(
                "Apparently you don't have a Moodle API Token, do you want to create one? Yes/No",
                "Your login and password won't be saved in the "
                "system, it'll be used to create your Token and the Encrypted Token will be stored",
            )
            await ctx.author.send(embed=embed)

            answer = await self.client.wait_for("message", check=check)

            if answer.content.lower() == "yes":
                embed = main_messages_style("Type and send your Moodle username")
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction(next(positive_emojis_list))

                username = await self.client.wait_for("message", check=check)

                embed = main_messages_style("Type and send your Moodle password")
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction(next(positive_emojis_list))

                password = await self.client.wait_for("message", check=check)

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

            loop_channel = await self.client.pg_con.fetch(
                "SELECT loop_channel FROM bot_servers",
            )

            for item in range(len((loop_channel))):  # Send on different servers
                if loop_channel[item]["loop_channel"]:
                    loop_channel = loop_channel[item]["loop_channel"]

                    if data and getData_Counter[0] % 16 == 0:
                        embed = main_messages_style(
                            f"Sending the Moodle events update {next(books_list)} {next(happy_faces)}"
                        )

                        await asyncio.sleep(0.5)

                        await self.client.get_channel(loop_channel).send(embed=embed)

                        amount = len(data)

                        for index in range(amount):
                            assignmentsdata = data_dict(data[index])

                            # Styling the message to improve user experience
                            color = moodle_color(index, assignmentsdata)

                            embed = check_command_style(
                                assignmentsdata, str(index + 1), color, None
                            )[0]

                            await asyncio.sleep(0.3)
                            await self.client.get_channel(loop_channel).send(
                                embed=embed
                            )

                        embed = main_messages_style(
                            f"There were a total of {amount} events {next(books_list)} see you in 8 hours {next(happy_faces)} ",
                            "Note: I am only showing events of 14 days ahead",
                        )

                        await asyncio.sleep(0.3)

                        await self.client.get_channel(loop_channel).send(embed=embed)

                    if not data and getData_Counter[0] % 16 == 0:
                        embed = main_messages_style(
                            "There weren't any scheduled events 😑😮",
                            "Note: This is really weird, be careful 🤨😶",
                        )

                        await asyncio.sleep(0.5)
                        await self.client.get_channel(loop_channel).send(embed=embed)

                    getData_Counter[0] += 1

        except AttributeError:
            pass

    @command(
        name="group",
        aliases=[
            "Group",
            "find_group",
            "FindGroup",
            "findGroup",
            "CreateGroup",
            "creategroup",
            "createGroup",
        ],
    )
    async def group(self, ctx, amount: int = None):
        if amount is None:
            embed = main_messages_style(
                "You must type the command plus the desired amount of members in the group",
                "Example: `--group 2`",
            )
            await ctx.send(embed=embed)

        else:

            embed = Embed(
                title="How to use it: ",
                description="To join this group you must react with the respective emoji",
                color=defaultcolor,
            )

            embed.set_author(name="Group Making Tool")

            embed.add_field(
                name=f"Member {emojis_list[0]}",
                value=f"`{ctx.author.display_name.capitalize()}`",
                inline=False,
            )

            for people in range(amount - 1):
                embed.add_field(
                    name=f"Member {emojis_list[people+1]}",
                    value=f"Click on the emoji to join as member {people+1}",
                    inline=False,
                )

            embed.set_footer(text=footer)

            msg = await ctx.send(embed=embed)

            for emoji in range(amount - 1):
                await msg.add_reaction(emojis_list[emoji + 1])

            await self.client.pg_con.execute(
                "INSERT INTO moodle_groups (message_id) VALUES ($1)", str(msg.id)
            )

            data = None

            try:
                data = await self.client.pg_con.fetch(
                    "SELECT discord_id FROM moodle_groups WHERE discord_id=$1 AND guild_id=$2",
                    ctx.author.id,
                    int(ctx.guild.id),
                )

            except Exception:
                pass

            if not data:
                await self.client.pg_con.execute(
                    "INSERT INTO moodle_groups (discord_id, discord_name, guild_id, guild_name, course, semester, class) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                    int(ctx.author.id),
                    str(ctx.author.display_name),
                    int(ctx.guild.id),
                    str(ctx.guild.name),
                    "CC",
                    "02",
                    "D",
                )

    # @Cog.listener()
    # async def on_raw_reaction_add(self, payload):

    #     try:
    #         message_id = await self.client.pg_con.fetch(
    #             "SELECT message_id FROM moodle_groups WHERE guild_id=$1",
    #             payload.guild_id,
    #         )
    #         message_is_list = [item for i in message_id for item in i]

    #     def check(reaction, user):
    #         return user == payload.author and (reaction.emoji) in emojis_list

    #     reaction, user = await self.client.wait_for("reaction_add", check=check)


def setup(client):
    client.add_cog(Moodle(client))
