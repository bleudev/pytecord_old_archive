"""
`context_menus.py`

In this file you will learn to create context menu in pytecord!
This is easier that commands ;)

Enjoy!
"""

# For start - create a client
from pytecord import Client
client = Client(token='token')

# import commands module:
from pytecord import app

# Import messages:
from pytecord import Message

# note: context menus is divided for 2 types: User and Message

# This is example message context menu
# warning: there are no descriptions in context menus!
# 'message: Message' is showing that command is message context menu
@client.context_menu()
async def message_context_menu(ctx: app.Context, message: Message):
    await ctx.send_message('Content:', message.content, '\n', 'Id:', message.id, ephemeral=True)

# Import users:
from pytecord import User

# This is example user context menu
# 'user: User' is showing that command is user context menu
@client.context_menu()
async def user_context_menu(ctx: app.Context, user: User):
    await ctx.send_message('Fullname:', str(user), '\n', 'Id:', user.id, ephemeral=True)

# Run the client
client.run()
