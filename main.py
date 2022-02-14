from requests import get
from yt_dlp import YoutubeDL
import discord
from discord.ext import commands
import logging
import asyncio

# bot setup
print(discord.__version__)
description = 'I have no enemies, merely topologies of ignorance!'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents, help_command=None)

# Error logging class, unused right now.
class ErrorLogging(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

# Queries youtube with passed search term or link and downloads an audio file in opus format.
def download_video(search):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
        }],
        'outtmpl': 'output.%(ext)s',
        'verbose': False,
        'logger': ErrorLogging(),
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            get(search)
        except:
            video = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]['webpage_url']
        else:
            video = search
        ydl.download([video])

# commands
@bot.event
async def on_ready():
    print("Behold! The great and powerful Elminster!")
    print(bot.user.name + '@%s' % bot.user.id)

@bot.command()
async def help(ctx):
    await ctx.send('Begin a request with \'$\' and I will dazzle you with my abilities!')

@bot.command()
async def play(ctx, *, search):
    download_video(search)
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("output.opus"), volume=0.1)
    if ctx.voice_client is None:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    ctx.voice_client.play(source)
    while ctx.voice_client.is_playing():
        await asyncio.sleep(.1)
    await ctx.voice_client.disconnect()

@bot.command()
async def developers(ctx):
    await ctx.send("DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS")
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("developers.opus"), volume=0.1)
    if ctx.voice_client is None:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    ctx.voice_client.play(source)

@bot.command()
async def dc(ctx):
    if ctx.voice_client is not None:
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send('Elminster shall take his leave!')
        else:
            await ctx.send('Silence knave, I\'m not in a voice channel.')

# discord.py logs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# open 
with open('./secret', 'r') as f:
    token = f.readline()
bot.run(token)
