from requests import get
import youtube_dl
import discord
from discord.ext import commands
import logging

# bot setup
print(discord.__version__)
description = 'I have no enemies, merely topologies of ignorance!'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents, help_command=None)

class ErrorLogging(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def download_video(search):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
        }],
        'outtmpl': 'output.%(ext)s',
        'verbose': True,
        'logger': ErrorLogging(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            get(search)
        except:
            video = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]['webpage_url']
        else:
            video = ydl.extract_info(search, download=False)
        ydl.download([video])

@bot.event
async def on_ready():
    print("Behold! The great and powerful Elminster!")
    print(bot.user.name + '@%s' % bot.user.id)

@bot.command()
async def help(ctx):
    await ctx.send('Begin a request with \'$\' and I will dazzle you with my abilities!')

@bot.command()
async def play(ctx, search):
    download_video(search)
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("output.opus"))

@bot.command()
async def developers(ctx):
    download_video("Developers")
    await ctx.send("DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS")

# discord.py logs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('./secret', 'r') as f:
    token = f.readline()
bot.run(token)
