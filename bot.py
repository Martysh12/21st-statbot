import nextcord
from nextcord.ext import commands

from dotenv import load_dotenv
import threading
import os

load_dotenv()

PREFIX = "statbot$"

HELP = f"""Help for StatBot:

`{PREFIX}help` - Show this message
`{PREFIX}set <mc/gmod/hl2dm>` - Set this channel for displaying a certain status
`{PREFIX}start` - Start displaying statuses
`{PREFIX}stop` - Stop displaying statuses

Status emojis, and what they mean:

🟢 - Server is online
🔴 - Server is offline
❌ - Could not fetch server data
🤔 - Fetching server data
"""

print("StatBot v1.0 by Martysh12#1610")
print("Created specifically for the Half-Life 2 - 21st Century Edition server.")

bot = commands.Bot(command_prefix=PREFIX, activity=nextcord.Game(PREFIX + "help"))
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Ready! Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def help(ctx):
    """Show help"""
    await ctx.send(HELP)

# @bot.command()
# async def ping(ctx):
#     await ctx.reply('Pong!')

bot.run(os.getenv("TOKEN"))
