"""
`basic_command.py`

In this file you will learn to create basic command in pytecord!
This is so easy ;)

Enjoy!
"""

# Imports
from pytecord import Client
from pytecord import Context

# Create a client
# note: You should replace 'token' to your token
client = Client(token='token')

# Create a command
#
# Doc is description of command (visible in discord)
# ctx - Context of command
# line 'await ctx.send_message("Hello, world!")' will send 'Hello, world!' message
@client.command()
async def basic_command(ctx: Context):
    """
    This is a basic command in pytecord!
    """
    await ctx.send_message('Hello, world!')

# Also you can add permissions that author must have
# For example, author must have administrator permission to use this command
@client.command('administrator')
async def command_only_for_admins(ctx: Context):
    """
    Command only for admins!
    """
    await ctx.send_message('You are admin!')

# Also you can create command with options!
# Doc describes command and his options
# '{name}: {type}' line is creating options (you may use basic python types)
@client.command()
async def command_with_options(ctx: Context, first: str, second: int = 15):
    """
    Command with options!

    Params:
        first: First option!
        second: Second option!
    """
    await ctx.send_message(first, second, ephemeral=True) # You may make message invisible for other users except author of interaction

# Run the client
client()
