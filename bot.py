import nextcord
from nextcord.ext import tasks, commands

from dotenv import load_dotenv

import requests

from datetime import datetime
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

start_first_time = True
start = False

@bot.event
async def on_ready():
    print(f'Ready! Logged in as {bot.user} (ID: {bot.user.id})')

@tasks.loop(minutes=10) # DAMN YOU WEIRD DISCORD CHANNEL RENAME RATE LIMIT! https://github.com/discord/discord-api-docs/issues/1900
async def check_servers():
    global start
    if start:
        print(f"[{datetime.now().strftime('%X')}] Updating channel names...")

        global mc_channel
        global gmod_channel
        global hl2dm_channel

        if mc_channel:
            mc_data = requests.get(APIS["mc"]).json()

            if mc_data["online"]:
                await mc_channel.edit(name=STATUS_SYMBOLS["online"] + mc_channel_original_name)
            else:
                await mc_channel.edit(name=STATUS_SYMBOLS["offline"] + mc_channel_original_name)

        if gmod_channel:
            gmod_data = requests.get(APIS["gmod"]).json()

            if gmod_data["online"]:
                await gmod_channel.edit(name=STATUS_SYMBOLS["online"] + gmod_channel_original_name)
            else:
                await gmod_channel.edit(name=STATUS_SYMBOLS["offline"] + gmod_channel_original_name)

        if hl2dm_channel:
            hl2dm_data = requests.get(APIS["hl2dm"]).json()

            if hl2dm_data["online"]:
                await hl2dm_channel.edit(name=STATUS_SYMBOLS["online"] + hl2dm_channel_original_name)
            else:
                await hl2dm_channel.edit(name=STATUS_SYMBOLS["offline"] + hl2dm_channel_original_name)

# MAIN COMMANDS #

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
        hl2dm_channel_original_name = ctx.channel.name
    else:
        await ctx.send(ERRORS["syntax"])
        return

    await ctx.send("Success!")

@bot.command()
async def unset(ctx):
    # look at this mess
    global mc_channel
    global gmod_channel
    global hl2dm_channel

    global mc_channel_original_name
    global gmod_channel_original_name
    global hl2dm_channel_original_name

    if ctx.channel.id == mc_channel.id:
        mc_channel = None
        mc_channel_original_name = None
    elif ctx.channel.id == gmod_channel.id:
        gmod_channel = None
        gmod_channel_original_name = None
    elif ctx.channel.id == hl2dm_channel.id:
        hl2dm_channel = None
        hl2dm_channel_original_name = None
    else:
        await ctx.send(ERRORS["notie"])
        return

    await ctx.send("Success!\nDue to weird Discord rate limits, you need to edit the channel name yourself to remove the emoji.")

@bot.command()
async def start(ctx):
    global start
    global start_first_time

    if start_first_time:
        check_servers.start()
        start_first_time = False

    start = True
    await ctx.send("Success!")

@bot.command()
async def stop(ctx):
    global start
    start = False
    await ctx.send("Success!")

@bot.command()
async def info(ctx):
    message = ""

    if mc_channel:
        message += f"Minecraft server: {mc_channel.mention}\n"
    if gmod_channel:
        message += f"GMod server: {gmod_channel.mention}\n"
    if hl2dm_channel:
        message += f"HL2DM server: {hl2dm_channel.mention}\n"

    await ctx.send(message if message else "There are currently no tied channels.")

#################

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(ERRORS["args"])
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(ERRORS["notfound"])

bot.run(os.getenv("TOKEN"))
