import nextcord
from nextcord.ext import commands

from dotenv import load_dotenv

import threading
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

bot.run(os.getenv("TOKEN"))
