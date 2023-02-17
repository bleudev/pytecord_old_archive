"""
`basic_command.py`

In this file you will learn to create basic command in disspy!
This is so easy ;)

Enjoy!
"""

# Import client
from disspy import Client

# Create a client
# note: You should replace 'token' to your token
client = Client(token='token')

# Import application commands module
from disspy import app

# Create a command!
# Docstring is description of command (visible in discord)
# ctx - Context of command
# line 'await ctx.send_message("Hello, world!")' will send 'Hello, world!' message
@client.command() # You may add `name` kwarg with your name. Else name will be function name
async def basic_command(ctx: app.Context):
    """
    This is a basic command in disspy!
    """
    await ctx.send_message('Hello, world!')

# Also you can create command with options!
# @app.describe(...) is describing your options
# '{name}: {type}' line is creating options (you may use basic python types)
@client.command()
@app.describe(
    first='First option!',
    second='Second option!'
)
async def command_with_options(ctx: app.Context, first: str, second: int = 15):
    """
    Command with options!
    """
    await ctx.send_message(first, second, ephemeral=True) # You may make message invisible for other users except author of interaction

# Run the client
client.run()
