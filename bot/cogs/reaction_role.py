import discord, asyncio
from discord.ext import tasks
from discord.ext.commands import command, Cog
from utilities import main_messages_style, footer, positive_emojis_list, defaultcolor



class reactionRole(Cog):

    def __init__(self,client):
        self.client = client

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 760608200386019338:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            
            if payload.emoji.name == "happy":
                role = discord.utils.get(guild.roles, name="Coder")

            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                await member.add_roles(role)
                print("role given")
            
            else:
                print("Role not found")


    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 760608200386019338:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            
            if payload.emoji.name == "happy":
                role = discord.utils.get(guild.roles, name="Coder")

            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                await member.remove_roles(role)
                print("role removed")
            
            else:
                print("Role not found")


    @command(name="CreateRoles", aliases=["ReactionRoles"])
    async def CreateRoles(self, ctx, amount):

        roles_list = []
        
        
        def check(ctx, m):
            return m.author == ctx.author

        embed = main_messages_style("Reaction Role Tool", "Type the Title for the command")
        await ctx.send(embed=embed)

        title = await self.client.wait_for('message')
        await ctx.channel.purge(limit=3)

        await asyncio.sleep(1)

        embed = main_messages_style("Reaction Role Tool", "Type the Description/Category for the roles")
        await ctx.send(embed=embed)


        main_description = await self.client.wait_for('message')

        await asyncio.sleep(1)
        await ctx.channel.purge(limit=2)

        for i in range(int(amount)):

            embed = main_messages_style("Reaction Role Tool", "Type the roles name")
            await ctx.send(embed=embed)

            Role = await self.client.wait_for('message')
            await ctx.channel.purge(limit=2)

            embed = main_messages_style("Reaction Role Tool", "Type the Emoji for the Role")
            await ctx.send(embed=embed)

            Emoji = await self.client.wait_for('message')
            await ctx.channel.purge(limit=2)

            embed = main_messages_style("Reaction Role Tool", "Type the roles Description")
            await ctx.send(embed=embed)

            Description = await self.client.wait_for('message')
            await ctx.channel.purge(limit=2)



            roles_dict = {
                "Emoji": Emoji.content,
                "Description": Description.content,
                "Role": Role.content
            }

            roles_list.append(roles_dict)
        

        embed = discord.Embed(title=title.content, description=main_description.content, color=defaultcolor)
        embed.set_author(name="Reaction Role")

        for item in range(int(amount)):
            embed.add_field(name=roles_list[item]["Role"] + " -  " + roles_list[item]["Emoji"] , value=roles_list[item]["Description"], inline=True)

        embed.set_footer(text=footer)
        menu = await ctx.send(embed=embed)

        menu_id = menu.id

        for item in range(int(amount)):
            emoji = roles_list[item]["Emoji"]
            await menu.add_reaction(emoji)


def setup(client):
    client.add_cog(reactionRole(client))