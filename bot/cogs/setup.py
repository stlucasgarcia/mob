from discord.ext.commands import Cog, command

from utilities import main_messages_style, positive_emojis_list, negative_emojis_list


class Setup(Cog):
    def __init__(self, client):
        self.client = client

    @command(name="preffix", aliases=["Preffix", "Prefix"])
    async def preffix(self, ctx, preffix=None):
        """Admin only command to change the server's preffix"""

        if preffix == None:

            server_preffix = await self.client.pg_con.fetch(
                "SELECT preffix FROM bot_servers WHERE guild_id = $1",
                ctx.guild.id,
            )

            server_preffix = server_preffix[0]["preffix"]

            embed = main_messages_style(
                f"The bot's preffix on this server is `{server_preffix}`",
                f"Note: You can change the server's preffix by using `{server_preffix}preffix + test` \n(instead of + test you type the preffix you want it to be)",
            )
            await ctx.send(embed=embed)

        else:
            await self.client.pg_con.execute(
                "UPDATE bot_servers SET preffix = $1 WHERE guild_id = $2",
                preffix,
                ctx.guild.id,
            )

            embed = main_messages_style(
                f"The bot's preffix on this server changed to `{preffix}`",
            )

            await ctx.send(embed=embed)

        await ctx.message.add_reaction(next(positive_emojis_list))

    @command(name="register", aliases=["Register", "Set_up", "set_up", "add_server"])
    async def register(self, ctx):
        """Admin only command, probably it can be used in case of the server did not register properly on the database"""
        try:
            await self.client.pg_con.execute(
                "INSERT INTO bot_servers (guild_id, guild_name, preffix) VALUES ($1, $2, $3)",
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


def setup(client):
    client.add_cog(Setup(client))
