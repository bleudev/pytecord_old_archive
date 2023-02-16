"""
`ready.py`

In this file you will learn to use `ready` event

Enjoy!
"""

# Create a client
from disspy import Client
client = Client(token='token') # Replace with your token

# For using events you can use `event` decorator
@client.event()
async def ready():
    print("Hello, i'm ready :3") # Print message on console

client.run()
