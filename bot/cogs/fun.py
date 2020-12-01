import discord
import random
import aiohttp

from discord.ext.commands import command, Cog
from random import randint

from utilities import (
    defaultcolor,
    main_messages_style,
    positive_emojis_list,
    negative_emojis_list,
)


class Fun(Cog):
    """Class(Cog) responsible for organizing fun commands"""

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
        """Gives a hug to another user or to yourself :)"""

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

    @command(name="cat", aliases=["Cat", "Kitty", "kitty", "Kitten", "kitten"])
    async def cat(self, ctx):
        """Gets a random picture of a cat"""

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
        aliases=[
            "Dog",
            "Doggo",
            "Doggy",
            "Puppy",
            "doggo",
            "doggy",
            "puppy",
            "pupper",
            "Pupper",
        ],
    )
    async def dog(self, ctx):
        """Gets a random picture of a dog"""

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
        """Gets a random picture of a fox"""

        embed = discord.Embed(color=defaultcolor)

        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as r:
                if r.status == 200:
                    data = await r.json()
                    await session.close()

        embed.set_image(url=data["image"])

        await ctx.send(embed=embed)

        await ctx.message.add_reaction(next(positive_emojis_list))

    @command(
        name="JoKenPo",
        aliases=[
            "jokenpo",
            "Jokenpo",
            "JoKenpo",
            "Rock_paper_scissors",
            "rock_paper_scissors",
            "roshambo",
            "Roshambo",
            "ro-sham-bo",
        ],
    )
    async def JoKenPo(self, ctx, option):
        """Rock, paper, scissors game where the user picks one and plays with the bot"""

        num = randint(1, 3)

        option = option.lower()

        if option == "rock":
            await ctx.message.add_reaction(next(positive_emojis_list))

            if num == 1:
                embed = main_messages_style(f"I picked `Rock`, it's a draw 😅 - 👊🏻👊🏻")
                await ctx.send(embed=embed)

            elif num == 2:
                embed = main_messages_style(f"I picked `Paper`, I won 😋 - 🧻👊🏻")
                await ctx.send(embed=embed)

            else:
                embed = main_messages_style(f"I picked `Scissors`, you won 😒 - ✂👊🏻")
                await ctx.send(embed=embed)

        elif option == "paper":
            await ctx.message.add_reaction(next(positive_emojis_list))

            if num == 1:
                embed = main_messages_style(f"I picked `Rock`, you won 🤬 - 👊🏻🧻")
                await ctx.send(embed=embed)

            elif num == 2:
                embed = main_messages_style(f"I picked `Paper`, it's a draw 😯 - 👊🏻🧻")
                await ctx.send(embed=embed)

            else:
                embed = main_messages_style(f"I picked `Scissors`, you lost 😄 - ✂🧻")
                await ctx.send(embed=embed)

        elif option == "scissors":
            await ctx.message.add_reaction(next(positive_emojis_list))

            if num == 1:
                embed = main_messages_style(f"I picked `Rock`, I won 🥱 - 👊🏻✂")
                await ctx.send(embed=embed)

            elif num == 2:
                embed = main_messages_style(f"I picked `Paper`, I lost 😨 - 🧻✂")
                await ctx.send(embed=embed)

            else:
                embed = main_messages_style(f"I picked `Scissors`, it's a draw 😶 - ✂✂")
                await ctx.send(embed=embed)

        else:
            await ctx.message.add_reaction(next(negative_emojis_list))

            embed = main_messages_style(
                "That's not a valid option",
                "Note: You must choose between rock, paper or scissors ",
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
