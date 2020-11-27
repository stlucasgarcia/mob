import discord
import asyncio

from discord.ext.commands import Cog, command
from discord.ext.commands.core import has_permissions
from discord import Embed
from utilities import (
    main_messages_style,
    timeout_message,
    positive_emojis_list,
    negative_emojis_list,
    footer,
    defaultcolor,
)
from secret1 import moodle_dict


class Setup(Cog):
    def __init__(self, client):
        self.client = client

    @command(name="prefix", aliases=["Prefix"])
    @has_permissions(administrator=True)
    async def prefix(self, ctx, prefix=None):
        """Admin only command to change the server's prefix"""

        if prefix is None:

            server_prefix = await self.client.pg_con.fetch(
                "SELECT prefix FROM bot_servers WHERE guild_id = $1",
                ctx.guild.id,
            )

            server_prefix = server_prefix[0]["prefix"]

            embed = main_messages_style(
                f"The bot's prefix on this server is `{server_prefix}`",
                f"Note: You can change the server's prefix by using `{server_prefix}prefix + test` \n(instead of + test you type the prefix you want it to be)",
            )
            await ctx.send(embed=embed)

        else:
            await self.client.pg_con.execute(
                "UPDATE bot_servers SET prefix = $1 WHERE guild_id = $2",
                prefix,
                ctx.guild.id,
            )

            embed = main_messages_style(
                f"The bot's prefix on this server changed to `{prefix}`",
            )

            await ctx.send(embed=embed)

        await ctx.message.add_reaction(next(positive_emojis_list))

    @command(name="register", aliases=["Register", "Set_up", "set_up", "add_server"])
    @has_permissions(administrator=True)
    async def register(self, ctx):
        """Admin only command, probably it can be used in case of the server did not register properly on the database"""

        try:
            await self.client.pg_con.execute(
                "INSERT INTO bot_servers (guild_id, guild_name, prefix) VALUES ($1, $2, $3)",
                int(ctx.guild.id),
                str(ctx.message.guild.name),
                "mack ",
            )

            embed = main_messages_style(
                f"The server {ctx.message.guild.name} is now registered",
                f"Note: You only need to use this command one time",
            )

            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(positive_emojis_list))

        except Exception:
            embed = main_messages_style(
                f"The server `{ctx.message.guild.name}` is already registered",
            )

            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(negative_emojis_list))

    @command(
        name="loop_channel",
        aliases=[
            "set_loop",
            "loopChannel",
            "setLoop",
            "Loop_Channel",
            "setLoopChannel",
        ],
    )
    @has_permissions(administrator=True)
    async def loop_channel(self, ctx):
        """Select the channel to send the getData loop (the moodle events)"""

        await self.client.pg_con.execute(
            "UPDATE bot_servers SET loop_channel = $1 WHERE guild_id = $2",
            ctx.channel.id,
            ctx.guild.id,
        )

        embed = main_messages_style(f"The loop channel is set to `#{ctx.channel.name}`")
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(next(positive_emojis_list))

    @command(
        name="moodleconfig",
        aliases=[
            "moodleConfig, moodle_config, MoodleConfig, setupMoodle, setup_moodle, setupmoodle"
        ],
    )
    @has_permissions(administrator=True)
    async def moodleconfig(self, ctx):
        """Sets up the server's moodle url"""

        embed = Embed(
            title="Select the server's moodle from the options below",
            description="React to your moodle's emoji to be ",
            color=defaultcolor,
        )
        embed.set_author(name="Moodle Configuration Tool")

        # Available options
        embed.add_field(
            name="Mackenzie <:mackenzie:771329600609189928>",
            value="Mackenzie main moodle",
            inline=True,
        )

        embed.set_footer(text=footer)
        menu = await ctx.send(embed=embed)

        emojis_list = ["<:mackenzie:771329600609189928>"]

        for index in range(len(emojis_list)):
            await menu.add_reaction(emojis_list[index])

        def check(reaction, user):
            return (
                reaction.message.id == menu.id
                and user == ctx.author
                and str(reaction.emoji) in emojis_list
            )

        timeout = 60.0
        try:
            opt = await self.client.wait_for(
                "reaction_add", timeout=timeout, check=check
            )
        except asyncio.TimeoutError:
            embed = timeout_message(timeout, reaction=True)
            return await ctx.send(embed=embed)

        i = emojis_list.index(str(opt[0]))
        url: str = ""

        if i == 0:
            url = moodle_dict["mackenzie"]

        await self.client.pg_con.execute(
            "UPDATE bot_servers SET moodle_url = $1 WHERE guild_id = $2",
            url,
            ctx.guild.id,
        )

        await ctx.message.add_reaction(next(positive_emojis_list))

    @command(
        name="auto_role",
        aliases=["AutoRole", "autoRole", "autorole", "auto_Role"],
    )
    @has_permissions(administrator=True)
    async def autoRole(self, ctx, role: discord.Role):
        """Sets up the server's 'on join' role"""
        if not role:
            embed = main_messages_style(
                "You need to type the roles name for this command",
                "Example: `autoRole Initialrole`",
            )
            await ctx.send(embed=embed)
            return

        else:
            role_id = discord.utils.get(ctx.guild.roles, name=role)

            await self.client.pg_con.execute(
                "UPDATE bot_servers SET on_join_role = $1 WHERE guild_id = $2",
                role_id,
                ctx.guild.id,
            )

            embed = main_messages_style(f"The on server's join role is set to {role}")
            await ctx.send(embed=embed)

    @command(
        name="loopTime",
        aliases=["looptime", "LoopTime", "loop_timer", "setLoopTimer", "setlooptimer"],
    )
    @has_permissions(administrator=True)
    async def loopTime(self, ctx, time):
        """Defines the time in minutes which getData loop will runs"""

        await self.client.pg_con.execute(
            "UPDATE bot_servers SET loop_time = $1 WHERE guild_id = $2",
            int(time),
            ctx.guild.id,
        )

        embed = main_messages_style(
            f"The server's getData loop is set to be every {int(time)} minutes"
        )
        await ctx.send(embed=embed)

    @command(name="setCourse", aliases=["SetCourse", "courseSet", "CourseSet", "setUpCourse", "setcourse", "courseset"])
    @has_permissions(administrator=True)
    async def setCourse(self, ctx, token):
        pass

def setup(client):
    client.add_cog(Setup(client))
