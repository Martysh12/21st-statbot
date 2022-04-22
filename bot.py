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
        mc_channel = ctx.channel
    elif which == "gmod":
        global gmod_channel
        gmod_channel = ctx.channel
    elif which == "hl2dm":
        global hl2dm_channel
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
