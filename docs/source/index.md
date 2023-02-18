```{toctree}
---
caption: Contents
maxdepth: 2
hidden:
---
index
objects/client
```

# Introduction

Discord is a social network. He has guilds, channels, users and other objects. Also there are bots in discord. For creating bots there are many libraries: discord.py, discord.js, hikari and other. Disspy also is a library for creating bots. In this documentation you learn foundations and peaks of this library.

Disspy is very easy library. For example, with this code you can receive and respond to messages that is sending in discord channel.

```py
import disspy

client = disspy.Client(token='token') # Replace with your token

@client.event
async def message(message: disspy.Message):
   await message.channel.send('Hello, world')

client()
```

*Really? Really simple code!*

:::{tip}
If you want to write some code and if you want to learn disspy, open 'Objects' folder.
:::