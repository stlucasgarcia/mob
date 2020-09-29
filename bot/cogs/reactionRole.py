import discord, asyncio
from discord.ext import tasks
from discord.ext.commands import command, Cog, has_permissions

class reactionRole(Cog):

    def __init__(self,client):
        self.client = client

    @Cog.listener()
    async def on_raw_reaction_add(payload):
        if payload.message_id == 760562128964550678:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
            
            role = discord.utils.get(guild.roles,name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                await member.add_roles(role)
                print("role given")
            
            else:
                print("Role not found")


def setup(client):
    client.add_cog(reactionRole(client))