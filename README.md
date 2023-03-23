# Pytecord
<p align=center>
    <img src="logo.png" width="200" alt="logo" style="text-align: center"/>
</p>
<p align=center>
    <img src="name.png" width="430" alt="logo" style="text-align: center"/>
</p>

[![Version](https://img.shields.io/badge/pypi-0.8-2C6CA6)](https://pypi.org/project/pytecord)
[![Project language](https://img.shields.io/badge/language-python-2C6CA6)](https://pypi.org/project/pytecord)
[![Python versions](https://img.shields.io/badge/python_versions-3.11-2C6CA6)](https://pypi.org/project/pytecord)
[![PyLint mark](https://img.shields.io/badge/pylink_mark-9.31/10-2C6CA6)](https://github.com/pixeldeee/pytecord/actions/workflows/pylint.yml)
[![Documenation status](https://readthedocs.org/projects/pytecord/badge/?version=latest)](https://pytecord.readthedocs.io/en/latest)
[![Code style: Black](https://img.shields.io/badge/code_style-black-black)](https://github.com/psf/black)

# Advantages
- Package with ``async/await`` support
- Wrappers and decorators support
- Simple code with syntax sugar
- Readable library code

# Getting started
Pytecord is package for creating bots in Discord. This package use discord API and discord Gateway
for handle events or, for example, sending messages. Bot use for different goals; handle information
on your server, creating mini games in discord, auto moderation in your discord server and other.

For example, you can reply to message that is sended by any user using this code:

```python
from pytecord import Client, Message  # Import library
import os

TOKEN = os.environ['TOKEN']
client = Client(TOKEN)  # Create a client

@client.on_message('create')  # On message create
async def on_messagec(message: Message):
    await message.reply('Hello!')  # Reply to the message

client.run()  # Run client
```

# Download package

## Download stable version

```command
# Windows
pip install -U pytecord

# MacOS / Linux
python3 -m pip install -U pytecord
```

## Download dev version (needs git)

```command
# Windows
git clone https://github.com/pixeldeee/pytecord.git
cd pytecord
pip install -U .

# MacOs / Linux
git clone https://github.com/pixeldeee/pytecord.git
cd pytecord
python3 -m pip install -U .
```

# Links

[Github](https://github.com/pixeldeee/pytecord) |
[PyPi](https://pypi.org/project/pytecord) |
[Docs](https://pytecord.readthedocs.io) |
[Discord](https://discord.gg/QsE5DSQrsx)