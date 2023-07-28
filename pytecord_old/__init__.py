'''
Pytecord is a libary for simple creating bot clients in discord API written in Python

Example client:
```
from pytecord import Client

client = Client(token='your_token')

@client.event
async def ready():
    print("Hello! I'm ready!")

client()
```

This bot will print "Hello! I'm ready!" string in console when it become ready

More examples you can find in `examples` directory on this link:


### Links

GitHub repo: https://github.com/pixeldeee/pytecord

More examples: https://github.com/pixeldeee/pytecord/tree/master/examples

PyPi: https://pypi.org/project/pytecord

Docs: https://pytecord.readthedocs.io/en/latest
'''

from pytecord.app import *
from pytecord.channel import *
from pytecord.client import *
from pytecord.profiles import *
from pytecord.role import *
from pytecord.ui import *
from pytecord.files import *
from pytecord.guild import *

# Info
__version__: str = '1.0-alpha-1'
__lib_name__: str = 'pytecord'
__lib_description__: str = (
    'Pytecord is a library for simple creating bot clients in discord API written in Python'
)
