import discord

from discord.ext.commands import command, Cog
from random import randint

from settings import allowed_channels
from utilities import defaultcolor, main_messages_style, positive_emojis_list


class Fun(Cog):
    def __init__(self, client):
        self.client = client

    @command(
        name="avatar",
        aliases=[
            "Avatar",
            "AVATAR",
            "avat",
            "profile_picture",
            "Profile_Picture",
            "p_picture",
            "profilePicture",
        ],
    )
    async def avatar(self, ctx, member: discord.Member = None):
        """Command to show someones avatar on the chat, you must mention the user"""

        if str(ctx.channel.id) in allowed_channels:
            member = ctx.author if not member else member

            embed = discord.Embed(color=defaultcolor)

            embed.set_image(url=f"{member.avatar_url}")

            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(positive_emojis_list))

    @command(
        name="e&o",
        aliases=[
            "Even_Or_Odd",
            "E&O",
            "even_or_odd",
            "e&O",
            "E&o",
            "even_and_odd",
            "Even_And_Odd",
        ],
    )
    async def Even_Or_Odd(self, ctx, option=None):
        """This command will pick randomly between ever or odd"""

        if str(ctx.channel.id) in allowed_channels:
            num = randint(1, 2)

            if num == 1:
                result = "Odd"

            else:
                result = "Even"

            if not option:
                embed = main_messages_style(
                    result, f"The bot picked {result} between even or odd"
                )

            elif option.lower() != "odd" or option.lower() != "even":
                if option.capitalize() == result:
                    embed = main_messages_style(
                        f"`{result}`, `{ctx.author.display_name}` won!!!🎉🥳🥳 ",
                        f"The bot picked `{result}` between even or odd",
                    )

                else:
                    embed = main_messages_style(
                        f"`{result}`, `{ctx.author.display_name}` lost 😥😪☹ ",
                        f"The bot picked `{result}` between even or odd",
                    )

            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(positive_emojis_list))

    @command(
        name="roll",
        aliases=["ROLL", "Roll", "Dice", "Roll_Dice", "dice", "rollDice", "roll_dice"],
    )
    async def roll(self, ctx, number=6):
        """Rolls a random number between 1 and the number you type"""

        if str(ctx.channel.id) in allowed_channels:
            embed = main_messages_style("Rolling dice... 🎲")

            await ctx.send(embed=embed)
            await ctx.channel.purge(limit=1)

            num = int(number)

            embed = main_messages_style(f"Your results were  `{randint(1,num)}`   🎲")
            await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))


def setup(client):
    client.add_cog(Fun(client))
