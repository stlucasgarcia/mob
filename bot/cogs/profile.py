import discord

from moodleapi.core.security.cryptography import Cryptography
from moodleapi.core.profile import get_user_profile
from discord.ext.commands import Cog, command

from utilities import main_messages_style, positive_emojis_list, negative_emojis_list
from utilities_moodle import moodle_profile_style


class Profile(Cog):
    """Class(Cog) responsible for managing the user's moodle profile and its dependencies"""

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def level_up(self, user):
        c_xp = user["experience"]
        c_lvl = user["level"]

        if c_xp >= round((4 * (c_lvl ** 3)) / 5):
            await self.client.pg_con.execute(
                "UPDATE bot_users SET level = $1 WHERE user_id = $2",
                c_lvl + 1,
                user["user_id"],
            )
            return True
        else:
            return False

    @Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.client.user or message.author.bot:
                return

            author_id = str(message.author.id)

            user = await self.client.pg_con.fetch(
                "SELECT * FROM bot_users WHERE user_id = $1",
                author_id,
            )

            if not user:
                await self.client.pg_con.execute(
                    "INSERT INTO bot_users (user_id, guild_id, level, experience, rep) VALUES ($1, $2, 1, 0, 0)",
                    author_id,
                    str(message.guild.id),
                )

            user = await self.client.pg_con.fetchrow(
                "SELECT * FROM bot_users WHERE user_id = $1",
                author_id,
            )

            await self.client.pg_con.execute(
                "UPDATE bot_users SET experience = $1 WHERE user_id = $2",
                user["experience"] + 1,
                author_id,
            )

            if await self.level_up(user):
                embed = main_messages_style(
                    f"{message.author.display_name} is now level {user['level'] + 1}!!"
                )
                await message.channel.send(embed=embed)

        except AttributeError:
            pass

    @command(name="profile", aliases=["Profile", "PROFILE", "Prof", "prof"])
    async def profile(self, ctx, member=None):
        """Profile command is used to show someones profile, levels and experience, you can mention another member to see his profile,
        leave it in blank to see your own or type someone's moodle username (TIA) to see his/hers moodle profile"""

        member = ctx.author if not member else member

        if str(member)[0].isnumeric():
            user_data = await self.client.pg_con.fetch(
                "SELECT token FROM moodle_profile WHERE discord_id = $1 AND guild_id = $2",
                ctx.author.id,
                ctx.guild.id,
            )

            if not user_data:
                embed = main_messages_style(
                    "You must create a token to use this command",
                    "Create a token by typing prefix + gettoken",
                )
                await ctx.send(embed=embed)

            token = Cryptography.decrypt(user_data[0]["token"])

            params = {
                "token": token,
                "tia": member,
                "url": "https://eadmoodle.mackenzie.br/webservice/rest/server.php?",
            }

            data = get_user_profile(**params)

            embed = moodle_profile_style(data)

            await ctx.send(embed=embed)

        else:
            member = (
                ctx.guild.get_member(int(member[3:-1]))
                if ctx.author != member
                else member
            )
            member_id = str(member.id)

            user = await self.client.pg_con.fetch(
                "SELECT * FROM bot_users WHERE user_id = $1",
                member_id,
            )

            user_level = user[0]["level"]
            user_experience = user[0]["experience"]
            xp_nextlvl = round((4 * (user_level ** 3)) / 5)
            rep = user[0]["rep"]

            if not user:
                await ctx.send("Member doesn't have a level")

            else:
                embed = discord.Embed(
                    color=member.color, timestamp=ctx.message.created_at
                )

                embed.set_thumbnail(url=member.avatar_url)

                embed.set_author(name=f"Profile - {member.display_name}")

                embed.add_field(name="Level", value=f"`{user_level}`")
                embed.add_field(name="XP", value=f"`{user_experience}/{xp_nextlvl}`")
                embed.add_field(name="Reputation", value=f"`{rep}`", inline=False)

                embed.add_field(
                    name=f"Messages Needed for level {user_level + 1}",
                    value=f"`{xp_nextlvl - user_experience}`",
                    inline=False,
                )

                embed.set_footer(text=f"{member}", icon_url=member.avatar_url)

                await ctx.send(embed=embed)

        await ctx.message.add_reaction(next(positive_emojis_list))

    @command(name="rep", aliases=["Rep", "Reputation", "reputation"])
    async def rep(self, ctx, member: discord.Member, opt: str = None):
        """Gives reputation to another user"""

        positive_options = ["+", "plus", "mais"]
        negative_options = ["-", "negative", "neg"]

        if opt and ctx.author.id != member.id:
            opt = opt.lower()

            rep = await self.client.pg_con.fetch(
                "SELECT rep FROM bot_users WHERE user_id = $1", str(member.id)
            )

            rep = rep[0]["rep"]

            if opt in positive_options:
                rep += 1
            elif opt in negative_options:
                rep -= 1
            else:
                embed = main_messages_style(
                    "Option not available" "Try using `+` or `-`"
                )
                await ctx.send(embed=embed)
                await ctx.message.add_reaction(next(negative_emojis_list))

                return

            await self.client.pg_con.execute(
                "UPDATE bot_users SET rep = $1 WHERE user_id = $2",
                rep,
                str(member.id),
            )

            embed = main_messages_style(
                f"{ctx.author.display_name} has given rep to {member.display_name}"
            )
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(positive_emojis_list))

        elif not opt and member.id != ctx.author.id:
            rep = await self.client.pg_con.fetch(
                "SELECT rep FROM bot_users WHERE user_id = $1", str(member.id)
            )

            rep = rep[0]["rep"]

            rep += 1

            await self.client.pg_con.execute(
                "UPDATE bot_users SET rep = $1 WHERE user_id = $2",
                rep,
                str(member.id),
            )

            embed = main_messages_style(
                f"{ctx.author.display_name} has given rep to {member.display_name}"
            )
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(positive_emojis_list))

        else:
            await ctx.message.add_reaction(next(negative_emojis_list))

            embed = main_messages_style(
                "Option not available", "Available options: `+` and `-`"
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Profile(client))
