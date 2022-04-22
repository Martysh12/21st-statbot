import nextcord
from nextcord.ext import tasks, commands

from dotenv import load_dotenv

import requests

import os

from constants import *

load_dotenv()

print("StatBot v1.0 by Martysh12#1610")
print("Created specifically for the Half-Life 2 - 21st Century Edition server.")

bot = commands.Bot(command_prefix=PREFIX, activity=nextcord.Game(PREFIX + "help"))
bot.remove_command('help')

mc_channel = None
gmod_channel = None
hl2dm_channel = None

mc_channel_original_name = ""
gmod_channel_original_name = ""
hl2dm_channel_original_name = ""

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

@bot.event
async def on_ready():
    print(f'Ready! Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def help(ctx):
    """Show help"""
    await ctx.send(HELP)

@bot.command()
async def set(ctx, which):
    """Set this channel for displaying a certain status"""
    error = False

    if which == "mc":
        global mc_channel
        global mc_channel_original_name

        mc_channel = ctx.channel
        mc_channel_original_name = ctx.channel.name
    elif which == "gmod":
        global gmod_channel
        global gmod_channel_original_name

        gmod_channel = ctx.channel
        gmod_channel_original_name = ctx.channel.name
    elif which == "hl2dm":
        global hl2dm_channel
        global hl2dm_channel_original_name

        hl2dm_channel = ctx.channel
    else:
        await ctx.send(ERRORS["syntax"])
        return

    await ctx.send("Success!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(ERRORS["args"])
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(ERRORS["notfound"])

# @bot.command()
# async def ping(ctx):
#     await ctx.reply('Pong!')

@tasks.loop(minutes=10) # DAMN YOU WEIRD DISCORD CHANNEL RENAME RATE LIMIT! https://github.com/discord/discord-api-docs/issues/1900
async def check_servers():
    global mc_channel
    global gmod_channel
    global hl2dm_channel

    if mc_channel:
        await mc_channel.edit(name=STATUS_SYMBOLS["fetching"] + mc_channel_original_name)
        mc_data = requests.get(APIS["mc"]).json()

        if mc_data["online"]:
            await mc_channel.edit(name=STATUS_SYMBOLS["online"] + mc_channel_original_name)
        else:
            await mc_channel.edit(name=STATUS_SYMBOLS["offline"] + mc_channel_original_name)

    if gmod_channel:
        await gmod_channel.edit(name=STATUS_SYMBOLS["fetching"] + gmod_channel_original_name)
        gmod_data = requests.get(APIS["gmod"]).json()

        if gmod_data["online"]:
            await gmod_channel.edit(name=STATUS_SYMBOLS["online"] + gmod_channel_original_name)
        else:
            await gmod_channel.edit(name=STATUS_SYMBOLS["offline"] + gmod_channel_original_name)

    if hl2dm_channel:
        await hl2dm_channel.edit(name=STATUS_SYMBOLS["fetching"] + hl2dm_channel_original_name)
        hl2dm_data = requests.get(APIS["hl2dm"]).json()

        if hl2dm_data["online"]:
            await hl2dm_channel.edit(name=STATUS_SYMBOLS["online"] + hl2dm_channel_original_name)
        else:
            await hl2dm_channel.edit(name=STATUS_SYMBOLS["offline"] + hl2dm_channel_original_name)

check_servers.start()

bot.run(os.getenv("TOKEN"))
