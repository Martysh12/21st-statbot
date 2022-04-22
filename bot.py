import nextcord
from nextcord.ext import commands

from dotenv import load_dotenv
import os

load_dotenv()

PREFIX = "statbot$"

print("StatBot v1.0 by Martysh12#1610")
print("Created specifically for the Half-Life 2 - 21st Century Edition server.")

bot = commands.Bot(command_prefix=PREFIX, activity=nextcord.Game(PREFIX + "help"))

@bot.command()
async def ping(ctx):
    await ctx.reply('Pong!')

bot.run(os.getenv("TOKEN"))
