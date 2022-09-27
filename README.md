# Dispy
<p align=center><img src="logo.png" width="430" alt="logo" style="text-align: center"/></p>

<p align=center>
    <a href="https://pypi.org/project/disspy">
        <img src="https://img.shields.io/badge/pypi-0.6-blueviolet?style=flat" alt="version"/>
    </a>
    <a href="https://pypi.org/project/disspy">
        <img src="https://img.shields.io/badge/language-python-blueviolet?style=flat" alt="project language"/>
    </a>
    <a href="https://pypi.org/project/disspy">
        <img src="https://img.shields.io/badge/python_versions-3.8_|_3.9_|_3.10-blueviolet?style=flat" alt="python version"/>
    </a>
    <a href="https://github.com/PyCQA/pylint">
        <img src="https://img.shields.io/badge/linting-pylint-blueviolet?style=flat" alt="linting"/></a>
    <a href="https://github.com/itttgg/dispy/actions/workflows/pylint.yml">
         <img src="https://img.shields.io/badge/pylink_mark-9.48/10-blueviolet?style=flat" alt="pylint mark"/>
    </a>
    <a href='https://disspy.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/disspy/badge/?version=latest' alt='documentation Status'/>
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code_style-black-black?style=flat" alt="Code style: black">
    </a>
</p>

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
from disspy import DisBot, DisMessage  # Import package
import os

TOKEN = os.environ["TOKEN"]
bot = DisBot(token=TOKEN)  # Create a bot

@bot.on_message("create")  # On message create
async def on_messagec(message: DisMessage):  # message - sended message
    await message.reply("Hello, world!")  # Reply to a message

bot.run()  # Run bot in Gateway
```

# Download package
## Download latest version (needs pip)

```command
# Windows
pip install -U disspy

# MacOS / Linux
python3 -m pip install -U disspy
```

## Download dev version (needs git and pip)

```command
# Windows
git clone https://github.com/itttgg/dispy.git
cd dispy
pip install -U .

# MacOs / Linux
git clone https://github.com/itttgg/dispy.git
cd dispy
python3 -m pip install -U .
```

# Links
<p><a href="https://github.com/itttgg/dispy">https://github.com/itttgg/dispy</a> - GitHub repo</p>
<p><a href="https://pypi.org/project/disspy">https://pypi.org/project/disspy</a> - Project site on PyPi</p>
<p><a href="https://disspy.readthedocs.io">https://disspy.readthedocs.io</a> - Site with docs for package</p>
<p><a href="https://discord.gg/QsE5DSQrsx">https://discord.gg/QsE5DSQrsx</a> - Discord server</p>
