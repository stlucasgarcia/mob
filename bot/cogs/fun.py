import discord
import random
import aiohttp

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

    @command(
        name="hug", aliases=["Hug", "Hugs", "hugs", "Send_Hug", "send_hug", "send_hugs"]
    )
    async def hug(self, ctx, member: discord.Member = None):
        if str(ctx.channel.id) in allowed_channels:
            if member:
                embed = main_messages_style(
                    f"{ctx.author.display_name} has sent a warm and comforting hug to {member.display_name}!🤗😊🥰",
                )

            else:
                embed = discord.Embed(color=defaultcolor)
                image = random.choice(
                    [
                        (
                            "https://media1.tenor.com/images/a1b6c954f41993410e4e2bf015e13fed/tenor.gif?itemid=4851066"
                        ),
                        (
                            "https://media1.tenor.com/images/b67b70e46deb55aef87a7c744e460373/tenor.gif?itemid=16316679"
                        ),
                        (
                            "https://media1.tenor.com/images/f77657e4f9d454de399b7c8acb1b8735/tenor.gif?itemid=7939501"
                        ),
                        (
                            "https://media1.tenor.com/images/0753413c29948bab6e9013fb70f6dd16/tenor.gif?itemid=14248948"
                        ),
                        (
                            "https://media1.tenor.com/images/c37397b49c003045c1bef4eb2999c739/tenor.gif?itemid=14712846"
                        ),
                        (
                            "https://media1.tenor.com/images/9e421b5fe5de23d27b7d9d6135b2dcd1/tenor.gif?itemid=16936183"
                        ),
                    ]
                )

                embed.set_image(url=image)

            await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))

    @command(name="cat", aliases=["Cat", "Kitty", "Kitten"])
    async def cat(self, ctx):
        if str(ctx.channel.id) in allowed_channels:

            embed = discord.Embed(color=defaultcolor)

            async with aiohttp.ClientSession() as session:
                async with session.get("http://aws.random.cat/meow") as r:
                    if r.status == 200:
                        data = await r.json()
                        await session.close()

            embed.set_image(url=data["file"])

            await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))

    @command(
        name="dog",
        aliases=["Dog", "Doggo", "Doggy", "Puppy", "doggo", "doggy", "puppy"],
    )
    async def dog(self, ctx):
        if str(ctx.channel.id) in allowed_channels:

            embed = discord.Embed(color=defaultcolor)

            isImage = False

            while not isImage:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://random.dog/woof.json") as r:
                        if r.status == 200:
                            data = await r.json()
                            await session.close()

                if data["url"].endswith(".mp4"):
                    pass

                else:
                    isImage = True

            embed.set_image(url=data["url"])

            await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))

    @command(name="fox", aliases=["Fox", "Floof", "floof", "Foxxy", "foxxy"])
    async def fox(self, ctx):
        if str(ctx.channel.id) in allowed_channels:

            embed = discord.Embed(color=defaultcolor)

            async with aiohttp.ClientSession() as session:
                async with session.get("https://randomfox.ca/floof/") as r:
                    if r.status == 200:
                        data = await r.json()
                        await session.close()

            embed.set_image(url=data["image"])

            await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))


def setup(client):
    client.add_cog(Fun(client))
