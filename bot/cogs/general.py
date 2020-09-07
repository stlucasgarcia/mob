import discord

from discord.ext import commands
from settings import *
from style import *


#status = cycle(["Estudando...", "Navegando no Moodle", "Descobrindo tarefas", "Dominando o mundo", "Reduzindo as suas faltas", "Calculando as suas médias"])

# General proposes bot commands 
class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Print in the console when the bot starts to run (if everything is working perfectly)
    @commands.Cog.listener()
    async def on_ready(self):
        print('The Bot is Online!')
        
        
    # @tasks.loop(seconds=5.0)
    # async def change(self):
    #     print("=============Foi=================")
    #     await self.client.change_presence(activity=discord.Game(next(status)))

    # Allow and disallow the text channel in which the bot can send messages, the variable is stored in /bot/settings.py
    @commands.command()
    async def permission(self, ctx, option=""):
        channel_id = ctx.channel.id
        option = option.lower()
        if option != "allow" and option != "disallow" and option == "":
            embed = main_messages_style("Option not available, you must use Allow or Disallow", "😕")
            await ctx.send(embed=embed)

        else:
            if option == "allow":
                if channel_id not in allowed_channels:
                    allowed_channels.append(ctx.channel.id)
                    embed = main_messages_style(f"Now I will operate on #{self.client.get_channel(ctx.channel.id)}")
                    await ctx.send(embed=embed)
                else:
                    embed =main_messages_style("I already operate on this channel")
                    await ctx.send(embed=embed)

            elif option == "disallow":
                if channel_id in allowed_channels:
                    allowed_channels.remove(ctx.channel.id)
                    embed = main_messages_style(f"I will no longer operate on #{self.client.get_channel(ctx.channel.id)}")
                    await ctx.send(embed=embed)
                else:
                    embed = main_messages_style("I already don't have permission to operate on this channel")
                    await ctx.send(embed=embed)            


    # Clear the previous line for x amout of times
    @commands.command()
    async def clear(self, ctx, amount=3):
        if ctx.channel.id in allowed_channels:
            await ctx.channel.purge(limit=amount)
            print("clear command")


def setup(client):
    client.add_cog(General(client))