import asyncio

from moodleapi import Mdl
from moodleapi.core.security import Token, Cryptography
from moodleapi.core.profile import get_user_profile

from discord.ext import tasks
from discord.ext.commands import command, Cog, cooldown
from settings import getData_Counter

from utilities import (
    main_messages_style,
    timeout_message,
    happy_faces,
    negative_emojis_list,
    books_list,
    positive_emojis_list,
    emojis_list,
)

from utilities_moodle import (
    data_dict,
    moodle_color,
    check_command_style,
    group_command_style,
    moodle_profile_style,
    get_data_timer,
)

# List with commands/functionalities related to the Moodle API
class Moodle(Cog):
    timer = get_data_timer[0]

    def __init__(self, client):
        self.client = client
        self.getData.start()
        self.moodle = Mdl()

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

                embed = check_command_style(assignmentsdata, str(index + 1), color)[0]
                await ctx.send(embed=embed)
                await asyncio.sleep(0.3)

            word = "were" if amount > 1 else "was"
            embed = main_messages_style(
                f"There {word} a total of {amount} {option} {next(books_list)}",
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

        decrypted_token = Cryptography.decrypt(token)

        self.moodle(
            decrypted_token,
            self.client.url,
            "core_calendar_get_calendar_day_view",  # "core_calendar_get_calendar_upcoming_view",
        )

        self.moodle.get(day=30, month=9, year=2020)

        embed = main_messages_style(f"Checking your assignments {next(books_list)} ...")
        await ctx.author.send(embed=embed)

        # Get data from the moodle and filter it
        self.moodle.export(
            db="moodle_assign",
            course="CCP",
            semester="02",
            clss="D",
            discord_id=user_id,
            guild_id=guild_id,
        )

        database = await self.client.pg_con.fetch(
            "SELECT * FROM moodle_assign WHERE discord_id = $1 AND guild_id = $2",
            user_id,
            guild_id,
        )

        # Check if there's assigns
        if database:
            await ctx.message.add_reaction(next(positive_emojis_list))

            amount = len(database)
            done = [0, 0]

            for index in range(amount):

                assignmentsdata = data_dict(database[index])

                # Style embed message
                color = moodle_color(index, assignmentsdata)

                embed, done = check_command_style(
                    assignmentsdata, str(index + 1), color, 1, done
                )

                await ctx.author.send(embed=embed)
                await asyncio.sleep(0.3)

            word = "classes" if done[1] > 1 else "class"
            embed = main_messages_style(
                f"You did {done[0]} out of {amount - done[1]} assignments and have {done[1]} {word} to attend {next(books_list)}",
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
            answer, username = None, None
            timeout = 45.0

            embed = main_messages_style(
                "Apparently you don't have a Moodle API Token, do you want to create one? Yes/No",
                "Your login and password won't be saved in the "
                "system, it'll be used to create your Token and the Encrypted Token will be stored",
            )
            await ctx.author.send(embed=embed)

            try:
                answer = await self.client.wait_for(
                    "message", timeout=timeout, check=check
                )
            except asyncio.TimeoutError:
                embed = timeout_message(timeout)
                return await ctx.author.send(embed=embed)

            if answer.content.lower() == "yes":
                embed = main_messages_style("Type and send your Moodle username")
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction(next(positive_emojis_list))

                try:
                    username = await self.client.wait_for(
                        "message", timeout=timeout, check=check
                    )
                except asyncio.TimeoutError:
                    embed = timeout_message(timeout)
                    return await ctx.author.send(embed=embed)

                embed = main_messages_style("Type and send your Moodle password")
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction(next(positive_emojis_list))

                try:
                    password = await self.client.wait_for(
                        "message", timeout=timeout, check=check
                    )
                except asyncio.TimeoutError:
                    embed = timeout_message(timeout)
                    return await ctx.author.send(embed=embed)

                # Call a function from moodleAPI to create a Token and save it encrypted on the file tokens.csv, it saves the discord author.id as well
                params = {
                    "discord_id": user_id,
                    "tia": username.content,
                    "course": "CCP",
                    "semester": "02",
                    "class": "D",
                    "guild_id": guild_id,
                }

                Token("https://eadmoodle.mackenzie.br/").create(
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

            decrypted_token = Cryptography.decrypt(token)

            embed = main_messages_style(
                f"Your decrypted Moodle API Token is, {decrypted_token}",
                "Note: You won't need to use it in this bot, your Token is already being used and it's stored in our database",
            )
            await ctx.author.send(embed=embed)

    # Gets Moodle data through Moodle API and send it to the chat
    # Loops the GetData function.
    @tasks.loop(minutes=timer)
    async def getData(self):
        CSmain = 169890240708870144

        try:
            tokens_data = await self.client.pg_con.fetch(
                "SELECT token FROM moodle_profile WHERE discord_id = $1", CSmain
            )

            token = tokens_data[0]["token"]

            decrypted_token = Cryptography.decrypt(token)

            # Get data from the moodle and filter it
            self.moodle(
                decrypted_token,
                self.client.url,
                "core_calendar_get_calendar_upcoming_view",
            )

            self.moodle.get(categoryid=2)

            self.moodle.export(
                db="moodle_events",
                course="CCP",
                semester="02",
                clss="D",
                discord_id=CSmain,
                guild_id=748168924465594419,
            )

            # Check if there's events
            data = await self.client.pg_con.fetch(
                "SELECT * FROM moodle_events WHERE discord_id = $1 AND guild_id = $2",
                CSmain,
                748168924465594419,
            )

            loop_channel = await self.client.pg_con.fetch(
                "SELECT loop_channel, loop_time FROM bot_servers",
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
        name="moodleUpdate",
        aliases=["moodle_update", "Update", "moodleupdate", "MoodleUpdate", "force"],
    )
    async def moodleUpdate(self, ctx):
        """Updates moodle data (assignments and classes)"""

        guild_id = ctx.guild.id

        CSmain = 169890240708870144

        tokens_data = await self.client.pg_con.fetch(
            "SELECT token FROM moodle_profile WHERE discord_id = $1", CSmain
        )

        token = tokens_data[0]["token"]

        decrypted_token = Cryptography.decrypt(token)

        # Get data from the moodle and filter it
        self.moodle(
            decrypted_token,
            self.client.url,
            "core_calendar_get_calendar_upcoming_view",
        )

        self.moodle.get(categoryid=2)

        self.moodle.export(
            db="moodle_events",
            course="CCP",
            semester="02",
            clss="D",
            discord_id=CSmain,
            guild_id=guild_id,
        )

        # Check if there's events
        await self.client.pg_con.fetch(
            "SELECT * FROM moodle_events WHERE discord_id = $1 AND guild_id = $2",
            CSmain,
            guild_id,
        )

        await ctx.message.add_reaction(next(positive_emojis_list))

        embed = main_messages_style("Moodle events updated successfully")
        await ctx.send(embed=embed)

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
        """Creates a group making which other students can join your group"""

        if amount is None:
            embed = main_messages_style(
                "You must type the command plus the desired amount of members in the group",
                "Example: `--group 2`",
            )
            await ctx.send(embed=embed)

        else:
            amount -= 1
            member = ctx.author.display_name.capitalize()

            await ctx.send("MENTION")

            embed = group_command_style(member, amount)
            msg = await ctx.send(embed=embed)

            for emoji in range(amount - 1):
                await msg.add_reaction(emojis_list[emoji + 1])

            await self.client.pg_con.execute(
                "INSERT INTO moodle_groups (msg_id, guild_id, member1, amount, channel_id) VALUES ($1, $2, $3, $4)",
                str(msg.id),
                ctx.guild.id,
                ctx.author.display_name,
                amount,
                ctx.channel.id,
            )

            await ctx.message.add_reaction(next(positive_emojis_list))

    # Group reaction checking
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Moodle group making 'waiting_for_reaction'"""

        message_id = await self.client.pg_con.fetch(
            "SELECT msg_id FROM moodle_groups WHERE guild_id=$1",
            payload.guild_id,
        )

        message_is_list = [item for i in message_id for item in i]

        if payload.message_id in message_is_list:
            data = await self.client.pg_con.fetch(
                "SELECT * from moodle_groups WHERE msg_id = $1", payload.message_id
            )
            print(data, len(data[0]))
            print(dir(payload))
            amount = int(data[0]["amount"])
            amount -= 1

            await self.client.pg_con.execute(
                f"UPDATE bot_groups SET member = $1 WHERE msg_id = $2",
                payload.user_id,
                payload.message_id,
                amount,
            )

            # embed = group_command_style(member, amount)
            # msg = await ctx.send(embed=embed)

            # for emoji in range(amount - 1):
            #     await msg.add_reaction(emojis_list[emoji + 1])

            # await self.client.pg_con.execute(
            #     "INSERT INTO moodle_groups (msg_id, guild_id, member1, amount) VALUES ($1, $2, $3, $4)",
            #     str(msg.id),
            #     ctx.guild.id,
            #     ctx.author.display_name,
            #     amount,
            # )

            # await self.client.pg_con.execute(
            #     "DELETE FROM moodle_groups WHERE msg_id = $1",
            #     str(msg.id),
            #     ctx.guild.id,
            #     ctx.author.display_name,
            #     amount,
            # )


def setup(client):
    client.add_cog(Moodle(client))
