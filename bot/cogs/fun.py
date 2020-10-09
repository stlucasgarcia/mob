import discord
from discord.ext.commands import command, Cog
from utilities import defaultcolor, main_messages_style, positive_emojis_list
from random import randint
from settings import allowed_channels


class Fun(Cog):
    
    def __init__(self, client):
        self.client = client


    @command(name="avatar", )
    async def avatar(self, ctx, member: discord.Member = None):
        """Command to show someones avatar on the chat, you must mention the user"""

        if str(ctx.channel.id) in allowed_channels:  
            member = ctx.author if not member else member

            embed = discord.Embed(color = defaultcolor)

            embed.set_image(url='{}'.format(member.avatar_url))
            
            await ctx.send(embed=embed)


    @command()
    async def even_or_odd(self,ctx):
        """This command will pick randomly between ever or odd"""

        if str(ctx.channel.id) in allowed_channels:  
            num = randint(1,2)
            if num == 1:
                embed = main_messages_style(f"Odd", "The bot picked Odd between even or odd")
            else:
                embed = main_messages_style(f"Even", "The bot picked Even between even or odd")

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))