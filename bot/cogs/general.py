import discord, asyncio
from discord.ext import tasks
from discord.ext.commands import command, Cog, has_permissions
from settings import allowed_channels
from utilities import main_messages_style, check_command_style, happy_faces, negative_emojis_list, books_list, positive_emojis_list, status_list 
import time
from typing import Optional

maincolor = None
# General use bot commands 
class General(Cog):
    def __init__(self, client):
        self.client = client


    # Print in the console when the bot starts to run (if everything is working perfectly)
    @Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ', self.client.user)
        print('ID:', self.client.user.id)
        self.change_status.start()

    #Discord live status that rotate from the list each 600 seconds
    @tasks.loop(seconds=600)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status_list)))


    # Allow, disallow or show the list of the text channel in which the bot can send messages, the variable is stored in /bot/settings.py
    @command(name="chat_permission",aliases=["c_permission", "chat_p", "chatpermission", "Chat_Permission", "Chat_P", "Chat_permission"])
    async def chat_permission(self, ctx, option=""):
        '''Gives the bot permission to work on that chat'''
        channel_id = str(ctx.channel.id)
        option = option.lower()
        if option != "allow" and option != "revoke" and option != "list" and option == "":
            embed = main_messages_style("Command **permission** allow or prohibit the bot messages on this chat","Option not available, you must use Allow, "
            "Prohibit or List ", " 😕")
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(negative_emojis_list))

        else:
            if option == "allow":
                guild_id = str(ctx.guild.id)
                if channel_id not in allowed_channels:
                    await self.client.pg_con.execute("INSERT INTO bot_data (allowed_channels, guild_id, bot_admin) VALUES ($1, $2, 226485287612710913)", channel_id, guild_id)
                    allowed_channels.append(channel_id)

                    embed = main_messages_style(f"Now I will operate on #{self.client.get_channel(ctx.channel.id)}")
                    await ctx.send(embed=embed)
                    await ctx.message.add_reaction(next(positive_emojis_list))

                else:
                    embed =main_messages_style("I already operate on this channel")
                    await ctx.send(embed=embed)
                    await ctx.message.add_reaction(next(negative_emojis_list))

            elif option == "revoke":
                if channel_id in allowed_channels:
                    await self.client.pg_con.execute("DELETE FROM bot_data WHERE allowed_channels = $1", channel_id)
                    allowed_channels.remove(channel_id)
                    embed = main_messages_style(f"I will no longer operate on #{self.client.get_channel(ctx.channel.id)}")
                    await ctx.send(embed=embed)
                    await ctx.message.add_reaction(next(positive_emojis_list))
                    
                else:
                    embed = main_messages_style("I already don't have permission to operate on this channel")
                    await ctx.send(embed=embed)            
                    await ctx.message.add_reaction(next(negative_emojis_list))

            elif option == "list":
                if channel_id in allowed_channels:
                    list_allowed = []

                    for i in range(len(allowed_channels)):
                        list_allowed.append(str(self.client.get_channel((int(allowed_channels[i])))))

                    if len(list_allowed) != 0:
                        str_list_allowed = ''
                        for elem in list_allowed:
                            str_list_allowed += elem + ',  #' if list_allowed.index(elem) != len(list_allowed)-1 else elem
                        
                        embed = main_messages_style(f"Channels allowed: #{str_list_allowed}")
                        await ctx.send(embed=embed)
                        await ctx.message.add_reaction(next(positive_emojis_list))
                else:
                    embed = main_messages_style(f"I don't have permission to chat here, type **mack Chat_permission allow** to give me the authorization to send messages and read commands in"
                    f" #{self.client.get_channel(ctx.channel.id)}")
                    await ctx.send(embed=embed)
                    await ctx.message.add_reaction(next(negative_emojis_list))


    #Clear the previous line for x amout of times
    @command(name="clear", aliases=["purge", "Clear", "CLEAR"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: Optional[int] = 2):
        """Cleans chat messages by any amount given"""
        await ctx.channel.purge(limit=amount)


    # Print an embed message on the chat
    @command(name="printm", aliases=["Print", "PrintM", "print", "Printmessage", "PRINT"])
    async def printm(self,ctx,name, message, emote=""):
        """Print a embed message"""
        channel_id = str(ctx.channel.id)

        if channel_id in allowed_channels:
            embed = main_messages_style(name, message, emote)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(next(positive_emojis_list))
        

    # Check latency/ping
    @Cog.listener()
    async def on_message(self,ctx):
        channel_id = str(ctx.channel.id)

        if channel_id in allowed_channels:
            if ctx.author == self.client.user:
                return
                
            if ctx.content.startswith("ping"):
                before = time.monotonic()

                embed = main_messages_style("Checking ping...")
                msg = await ctx.channel.send(embed=embed)

                ping = (time.monotonic() - before) * 1000
                await ctx.channel.purge(limit=1)

                embed = main_messages_style(f"Pong!  🏓  `{int(ping)}ms`")
                await ctx.channel.send(embed=embed)
                
                print(f'Ping {int(ping)}ms')



def setup(client):
    client.add_cog(General(client))