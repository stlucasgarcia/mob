import discord
Bot_token = 'NzQ1ODAzOTMxMDk5MzMyNjM4.Xz3GCQ.uUA2Eck1PK1-9pRizBt-gfuRaUQ'
PrefixCommands = '-m'
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PrefixCommands):
        await message.channel.send('Mackenzie bot a sua disposicao!')

client.run(Bot_token)
