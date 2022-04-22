PREFIX = "statbot$"

HELP = f"""Help for StatBot:

`{PREFIX}help` - Show this message
`{PREFIX}set <mc/gmod/hl2dm>` - Set this channel for displaying a certain status
`{PREFIX}start` - Start displaying statuses
`{PREFIX}stop` - Stop displaying statuses
`{PREFIX}info` - Show channels with a statues tied to them
`{PREFIX}serverinfo <mc/gmod/hl2dm>` - Show server info

Status emojis, and what they mean:

🤢 - Server is online
🥵 - Server is offline
🗿 - Could not fetch server data
🤔 - Fetching server data
"""

ERRORS = {
    "syntax": f"Syntax error! Refer to `{PREFIX}help`",
    "args": f"Not enough arguments! Refer to `{PREFIX}help`",
    "notfound": f"Command not found! Refer to `{PREFIX}help`"
}

APIS = {
    "mc": "https://api.dominic.sk/v1/ping/mc",
    "gmod": "https://api.dominic.sk/v1/ping/gmod",
    "hl2dm": "https://api.dominic.sk/v1/ping/hl2dm"
}

STATUS_SYMBOLS = {
    "online": "🤢",
    "offline": "🥵",
    "error": "🗿",
    "fetching": "🤔"
}
