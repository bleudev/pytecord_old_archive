"""
`context_menus.py`

In this file you will learn to create context menu in pytecord!
This is easier that commands ;)

Enjoy!
"""

# Imports
from pytecord import Client, Context

# Create a client
client = Client(token='token')

# Import messages:
from pytecord import Message

# note: context menus is divided for 2 types: User and Message

# This is example message context menu
# warning: there are no descriptions in context menus!
# 'message: Message' is showing that command is message context menu
@client.context_menu()
async def message_context_menu(ctx: Context, message: Message):
    await ctx.send_message(
        'Content:', message.content, '\n',
        'Id:', message.id,
        ephemeral=True
    )

# Import users:
from pytecord import User

# This is example user context menu
# 'user: User' is showing that command is user context menu
@client.context_menu()
async def user_context_menu(ctx: Context, user: User):
    await ctx.send_message(
        'Fullname:', user, '\n',
        'Id:', user.id,
        ephemeral=True
        )

# Run the client
client()
