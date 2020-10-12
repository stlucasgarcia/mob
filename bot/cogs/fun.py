import discord
from discord.ext.commands import command, Cog
from utilities import defaultcolor, main_messages_style, positive_emojis_list
from random import randint
from settings import allowed_channels
from random import randint


class Fun(Cog):
    
    def __init__(self, client):
        self.client = client


    @command(name="avatar", aliases=["Avatar", "AVATAR", "avat", "profile_picture", "Profile_Picture", "p_picture", "profilePicture"])
    async def avatar(self, ctx, member: discord.Member = None):
        """Command to show someones avatar on the chat, you must mention the user"""

        if str(ctx.channel.id) in allowed_channels:  
            member = ctx.author if not member else member

            embed = discord.Embed(color = defaultcolor)

            embed.set_image(url='{}'.format(member.avatar_url))
            
            await ctx.send(embed=embed)


    @command(name="e&o", aliases=["Even_Or_Odd", "E&O", "even_or_odd", "e&O", "E&o", "even_and_odd", "Even_And_Odd"])
    async def Even_Or_Odd(self,ctx):
        """This command will pick randomly between ever or odd"""

        if str(ctx.channel.id) in allowed_channels:  
            num = randint(1,2)
            if num == 1:
                embed = main_messages_style(f"Odd", "The bot picked Odd between even or odd")
            else:
                embed = main_messages_style(f"Even", "The bot picked Even between even or odd")

            await ctx.send(embed=embed)
    #TODO pick between even or odd then says if won or lost

    @command(name="roll", aliases=["ROLL", "Roll", "Dice", "Roll_Dice", "dice", "rollDice", "roll_dice"])
    async def roll(self,ctx, number=6): #Sets default roll number to 6
        """Rolls a random number between 1 and the number you type"""

        if str(ctx.channel.id) in allowed_channels:
            embed = main_messages_style("Rolling dice... 🎲")

            await ctx.send(embed=embed)
            await ctx.channel.purge(limit=1)

            num = int(number)

            await ctx.message.add_reaction(next(positive_emojis_list))
            embed = main_messages_style(f"Your results were  `{randint(1,num)}`   🎲")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))