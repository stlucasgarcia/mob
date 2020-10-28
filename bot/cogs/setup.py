from discord.ext.commands import Cog, command
from discord.ext.commands.core import has_permissions

from utilities import main_messages_style, positive_emojis_list, negative_emojis_list


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


def setup(client):
    client.add_cog(Setup(client))
