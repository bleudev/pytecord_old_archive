# Dispy
<p align=center><img src="logo.png" width="430" alt="logo" style="text-align: center"/></p>

[![Version](https://img.shields.io/badge/pypi-0.8-2C6CA6)](https://pypi.org/project/disspy)
[![Project language](https://img.shields.io/badge/language-python-2C6CA6)](https://pypi.org/project/disspy)
[![Python versions](https://img.shields.io/badge/python_versions-3.8_|_3.9_|_3.10_|_3.11-2C6CA6)](https://pypi.org/project/disspy)
[![PyLint mark](https://img.shields.io/badge/pylink_mark-9.31/10-2C6CA6)](https://github.com/pixeldeee/disspy/actions/workflows/pylint.yml)
[![Documenation status](https://readthedocs.org/projects/disspy/badge/?version=latest)](https://disspy.readthedocs.io/en/latest)
[![Code style: Black](https://img.shields.io/badge/code_style-black-black)](https://github.com/psf/black)

# Advantages
- Package with ``async/await`` support
- Wrappers and decorators support
- Simple code with syntax sugar
- Minimal python version is 3.8
- Readable library code

# Getting started
Dispy is package for creating bots in Discord. This package use discord API and discord Gateway
for handle events or, for example, sending messages. Bot use for different goals; handle information
on your server, creating mini games in discord, auto moderation in your discord server and other.

For example, you can reply to message that is sended by any user using this code:

```python
from disspy import Client, Message  # Import library
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
pip install -U disspy

# MacOS / Linux
python3 -m pip install -U disspy
```

## Download dev version (needs git)

```command
# Windows
git clone https://github.com/pixeldeee/disspy.git
cd dispy
pip install -U .

# MacOs / Linux
git clone https://github.com/pixeldeee/disspy.git
cd dispy
python3 -m pip install -U .
```

# Links

[Github](https://github.com/pixeldeee/disspy) |
[PyPi](https://pypi.org/project/disspy) |
[Docs](https://disspy.readthedocs.io) |
[Discord](https://discord.gg/QsE5DSQrsx)