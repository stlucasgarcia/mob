import discord
from discord.ext.commands import Cog, command


class Levels(Cog):
    def __init__(self, client):
        self.client = client
    
    @Cog.listener()
    async def level_up(self, user):
        c_xp = user["experience"]
        c_lvl = user["level"]

        if c_xp >= round((4 * (c_lvl ** 3)) / 5):
            await self.client.pg_con.execute("UPDATE bot_users SET level = $1 WHERE user_id = $2 AND guild_id = $3", c_lvl + 1, user["user_id"], user["guild_id"])
            return True
        else:
            return False
    
    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM bot_users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)

        if not user:
            await self.client.pg_con.execute("INSERT INTO bot_users (user_id, guild_id, level, experience) VALUES ($1, $2, 1, 0)", author_id, guild_id)


        user = await self.client.pg_con.fetchrow("SELECT * FROM bot_users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)

        await self.client.pg_con.execute("UPDATE bot_users SET experience = $1 WHERE user_id = $2 AND guild_id = $3", user['experience'] + 1, author_id, guild_id)

        if await self.level_up(user):
            await message.channel.send(f"{message.author.mention} is now level {user['level'] + 1}")
        

    @command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM bot_users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)


        if not user:
            await ctx.send("Member doens't have a level")
        else:
            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

            embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)

            embed.add_field(name="Level", value=user[0]["level"])
            embed.add_field(name="XP", value=user[0]["experience"])
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Levels(client))