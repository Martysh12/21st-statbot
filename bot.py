import nextcord
from nextcord.ext import tasks, commands

from dotenv import load_dotenv

import requests

from datetime import datetime
import os
import re

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

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

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
@commands.check_any(commands.has_role(966442031075459072), commands.is_owner())
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
@commands.check_any(commands.has_role(966442031075459072), commands.is_owner())
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
@commands.check_any(commands.has_role(966442031075459072), commands.is_owner())
async def start(ctx):
    global start
    global start_first_time

    if start_first_time:
        check_servers.start()
        start_first_time = False

    start = True
    await ctx.send("Success!")

@bot.command()
@commands.check_any(commands.has_role(966442031075459072), commands.is_owner())
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

@bot.command()
async def serverinfo(ctx):
    mc_data = requests.get(APIS["mc"]).json()
    gmod_data = requests.get(APIS["gmod"]).json()
    hl2dm_data = requests.get(APIS["hl2dm"]).json()

    server_embed = nextcord.Embed(title="Servers")

    server_embed.add_field(name="-" * len(mc_data["server"]), value=mc_data["server"], inline=False)
    server_embed.add_field(name="Online", value=mc_data["online"], inline=True)
    server_embed.add_field(name="Operator", value=mc_data["operator"], inline=True)

    if mc_data["online"]:
        server_embed.add_field(name="Players", value=f"{mc_data['players']['players_online']}/{mc_data['players']['players_max']}", inline=True)
        server_embed.add_field(name="Network protocol", value=str(mc_data["server_info"]["protocol"]), inline=True)
        server_embed.add_field(name="Version", value=mc_data["server_info"]["server_version"], inline=True)

    server_embed.add_field(name="-" * len(gmod_data["server"]), value=gmod_data["server"], inline=False)
    server_embed.add_field(name="Online", value=gmod_data["online"], inline=True)
    server_embed.add_field(name="Operator", value=gmod_data["operator"], inline=True)

    server_embed.add_field(name="-" * len(hl2dm_data["server"]), value=hl2dm_data["server"], inline=False)
    server_embed.add_field(name="Online", value=hl2dm_data["online"], inline=True)
    server_embed.add_field(name="Operator", value=hl2dm_data["operator"], inline=True)

    server_embed.set_footer(text="Bot by Martysh12#1610")

    await ctx.send(embed=server_embed)

@bot.command()
async def credits(ctx):
    await ctx.send("Programmed by: Martysh12#1610 and NotDominic#4952\nIf you encounter any errors, feel free to DM us :)")

@bot.command()
async def removeemojis(ctx):
    await ctx.channel.edit(name=remove_emojis(ctx.channel.name))
    await ctx.send("Success!")

#################

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(ERRORS["args"])
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(ERRORS["notfound"])

bot.run(os.getenv("TOKEN"))
