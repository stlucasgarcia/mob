import discord
from discord.ext.commands import command, Cog
from utilities import defaultcolor


class Fun(Cog):
    
    def __init__(self, client):
        self.client = client

    # Command to show someones avatar on the chat
    @command()
    async def avatar(self, ctx, member: discord.Member = None):
        
        member = ctx.author if not member else member

        embed = discord.Embed(color = defaultcolor)

        embed.set_image(url='{}'.format(member.avatar_url))
        
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))