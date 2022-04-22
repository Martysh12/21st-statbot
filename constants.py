PREFIX = "statbot$"

HELP = f"""Help for StatBot:

`{PREFIX}help` - Show this message
`{PREFIX}set <mc/gmod/hl2dm>` - Tie status to channel
`{PREFIX}unset` - Untie status from channel
`{PREFIX}start` - Start displaying all statuses
`{PREFIX}stop` - Stop displaying all statuses
`{PREFIX}info` - Show all channels with a status tied to them
`{PREFIX}serverinfo` - Show info about all servers

Status emojis, and what they mean:

🟢 - Server is online
🔴 - Server is offline
"""

ERRORS = {
    "syntax": f"Syntax error! Refer to `{PREFIX}help`",
    "args": f"Not enough arguments! Refer to `{PREFIX}help`",
    "notfound": f"Command not found! Refer to `{PREFIX}help`",
    "notie": f"No statues tied to this channel!"
}

APIS = {
    "mc": "https://api.dominic.sk/v1/ping/mc",
    "gmod": "https://api.dominic.sk/v1/ping/gmod",
    "hl2dm": "https://api.dominic.sk/v1/ping/hl2dm"
}

STATUS_SYMBOLS = {
    "online": "🟢",
    "offline": "🔴",
    "error": "⚫"
}
