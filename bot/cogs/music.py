import youtube_dl, discord, asyncio, os, datetime

from discord.ext import tasks
from discord.ext.commands import Cog, command, CommandError
from discord.voice_client import VoiceClient
from discord.utils import get


from utilities import main_messages_style, positive_emojis_list, defaultcolor, footer, formatTime
from settings import allowed_channels


youtube_dl.utils.bug_reports_message = lambda: ''

# Basic format options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    # 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', # In case of connection error
    'options': '-vn'
}


ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

songs = asyncio.Queue()

play_next_song = asyncio.Event()

queues = {}


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data 

        self.title = data.get('title') 

        self.url = data.get('url') 

        self.duration = data.get('duration')

        self.thumbnail = data.get('thumbnail') 

        self.webpage_url = data.get('webpage_url')

        self.view_count = data.get('view_count')

        self.uploader = data.get('uploader')



    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=True))

        if 'entries' in data:
            data = data['entries'][0]

        file =  ytdl.prepare_filename(data)

        return cls(discord.FFmpegPCMAudio(file, **ffmpeg_options), data=data)



class Music(Cog):
    def __init__(self, client):
        self.client = client


    @command(name="join", aliases=["JOIN", "Join", "Connect", "connect"])
    async def join(self, ctx):
        """Join command is used to make the bot join to the voice chat which you're in"""

        if str(ctx.channel.id) in allowed_channels:

            channel = ctx.message.author.voice.channel

            if not channel:
                embed = main_messages_style(f"{ctx.author.capitalize()} is not connected to a voice channel")
                await ctx.send(embed=embed)
                return

            voice = get(self.client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()
                voice = await channel.connect()

                embed = main_messages_style(f"The bot moved to `{channel}`")
                await ctx.send(embed=embed)

            else:
                voice = await channel.connect()

                embed = main_messages_style(f"The bot is now connected to `{channel}`")
                await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))

    
    @command(name="leave", aliases=["LEAVE", "Leave", "disconnect", "Disconnect"])
    async def leave(self, ctx):
        """Leave command is used to make the bot disconnect from any voice chat"""

        if str(ctx.channel.id) in allowed_channels:

            channel = ctx.message.author.voice.channel

            voice = get(self.client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():

                await voice.disconnect()

                embed = main_messages_style(f"The bot is now disconnected from `{channel}`")
                await ctx.send(embed=embed)

            else:
                embed = main_messages_style("The bot is not connected to any voice channel")
                await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))


    @command(name="play", aliases=["Play", "PLAY"])
    async def play(self, ctx, *, url):
        """Makes the bot play a song by youtube link/search"""

        #TODO Verification for *, url

        if str(ctx.channel.id) in allowed_channels:

            channel = ctx.message.author.voice.channel

            queues[ctx.guild.id] = songs

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.client.loop)

                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)


                 
                print("{:,}".format(int(player.view_count)))

                        
                embed= discord.Embed(title=player.title, color=defaultcolor)
                embed.set_author(name="Now playing:")
                embed.add_field(name="Link", value=f"{player.webpage_url}", inline=False)
                embed.add_field(name="Duration", value=f"`{formatTime((player.duration))}`", inline=True)
                embed.add_field(name="Views", value="`{:,}`".format(int(player.view_count)), inline=True)
                embed.add_field(name="Channel", value=f"`{player.uploader}`", inline=True)

                embed.set_image(url=player.thumbnail)
                embed.set_footer(text=footer)

                pMessage = await ctx.send(embed=embed)

                await pMessage.add_reaction("⏪")
                await pMessage.add_reaction("▶")
                await pMessage.add_reaction("⏩")

                await queues[ctx.guild.id].put(player)


            await ctx.message.add_reaction(next(positive_emojis_list))

    @command(name="volume", aliases=["vol, Volume", "Vol"])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if str(ctx.channel.id) in allowed_channels:

            if ctx.voice_client is None:
                embed = main_messages_style("The bot is not connected to a voice channel")
                return await ctx.send(embed=embed)

            ctx.voice_client.source.volume = volume / 100

            embed = main_messages_style(f"Changed volume to `{volume}`")
            await ctx.send(embed=embed)

            await ctx.message.add_reaction(next(positive_emojis_list))

    @play.before_invoke
    async def check_ifvoiceChannel(self, ctx):
        if ctx.voice_client is None:

            if ctx.author.voice:
                await ctx.author.voice.channel.connect()

        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        # Delete older songs (that are not in queue) .webm
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(".webm"):
                os.remove(f'{os.getcwd()}/{filename}')


#TODO Queue system, Fix permission error

def setup(client):
    client.add_cog(Music(client))