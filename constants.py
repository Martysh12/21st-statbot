PREFIX = "statbot$"

HELP = f"""Help for StatBot:

`{PREFIX}help` - Show this message
`{PREFIX}set <mc/gmod/hl2dm>` - Set this channel for displaying a certain status
`{PREFIX}start` - Start displaying statuses
`{PREFIX}stop` - Stop displaying statuses
`{PREFIX}info` - Show channels with a statues tied to them

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
