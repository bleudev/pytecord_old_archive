# Dispy
<p align=center><img src="imgs/logo.png" width="430" alt="logo" style="text-align: center"/></p>

<p align=center>
    <img src="https://img.shields.io/badge/pypi-0.5.3-blueviolet?style=flat" alt="version"/>
    <img src="https://img.shields.io/badge/lang-python-blueviolet?style=flat" alt="project language"/>
    <img src="https://img.shields.io/badge/python_version-3.8 and higher-blueviolet?style=flat" alt="python version"/>
    <img src="https://img.shields.io/badge/linting_tool-pylint-blueviolet?style=flat" alt="linting tool"/>
    <img src="https://img.shields.io/badge/pylink_mark_(3.8)-8.33/10-blueviolet?style=flat" alt="pylint mark"/>
    <a href='https://dispy-api-docs.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/dispy-api-docs/badge/?version=latest' alt='documentation Status' />
    </a>
</p>

# Advantages
- Package for ``async/await`` support
- Registering events with wrappers
- Easy code with syntax sugar

## Needs minimal 3.8 python version
Dispy is package for creating bots in Discord. This package use discord API and discord Gateway
for handle events or, for example, sending messages. Bot use for different goals; handle information
on your server, creating mini games in discord, auto moderation in your discord server and other.
For example, you can send messages use this code:
```python
import disspy  # Import package

bot = disspy.DisBot(token="YOUR_TOKEN", application_id=00000)  # Create a bot

async def test():  # Send messages needs to execute in the async function
    channel_id = 000000  # Yours channel id
    channel = bot.get_channel(channel_id)  # Get the channel for sending to this channel a message
    
    await channel.send(content="Message!")  # Sending a message
    
if __name__ == '__main__':  # If file is started as a main file
    from asyncio import run  # Import asyncio.run
    
    run(test())  # Run async function

# Download package
## Download stable version
```
# Windows
pip install --upgrade disspy

# MacOS
py3 -m pip install --upgrade disspy

# Lunix
sudo pip install --upgrade disspy
```

## Download dev version
```
git clone https://github.com/itttgg/dispy.git
cd dispy
pip install --upgrade .
```

# Links
<p><a href="https://github.com/itttgg/dispy">https://github.com/itttgg/dispy</a> - GitHub repo</p>
<p><a href="https://pypi.org/project/disspy">https://pypi.org/project/disspy</a> - Project site on PyPi</p>
<p><a href="https://dispy-api-docs.readthedocs.io/en/latest">https://dispy-api-docs.readthedocs.io/en/latest</a> - Site with docs for package</p>
# Using
### Creating and running bot

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN")

bot.run()
```

### bot.on("ready")

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN")


@bot.on("ready")
async def on_ready():
    print("Ready!")


bot.run()
```

### bot.on("messagec")
*message create event*

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN", flags=disspy.DisFlags.messages())


@bot.on("messagec")
async def on_messagec(message: disspy.DisMessage):
    await message.channel.send("Content: " + message.content)


bot.run()
```

### bot.on("messageu")
*message update event*

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN", flags=disspy.DisFlags.messages())


@bot.on("messageu")
async def on_messageu(message: disspy.DisMessage):
    await message.channel.send("New content of message: " + message.content)


bot.run()
```

### bot.on("messaged")
*message delete event*

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN", flags=disspy.DisFlags.messages())


@bot.on("messaged")
async def on_messaged(e: disspy.MessageDeleteEvent):
    await e.channel.send("You deleted message!")


bot.run()
```
