"""
`get_started.py`

This is a file for learn how to get started in pytecord

Just read this file :)
Enjoy!
"""

# For get started import library
import pytecord

# Also you can import any things using `from`
from pytecord import Client

# Let's create client!
# 1 step: Copy token from Discord Developer Portal
#
# I will use environ for getting token
# For using this lines, create enviroment variable named `token` with your token value
from os import environ
TOKEN = environ['token']

# 2 step: create `client` variable (or any other name)
client = Client(token=TOKEN)

# 3 step: Append events
# You can set name of the event using `name` argument or pytecord will take function name
#
# async def ready()
#           ^^^^^^^
# this means that event is `ready` event
@client.event
async def ready():
    print('Hi')
# This code wil print 'Hi' in console when client becomes ready

# 4 step: run client
# For start client work, it must be ran
client.run()

# Success!
# Now you know how start in pytecord
# This is the end of file
