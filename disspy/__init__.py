'''
Disspy is a libary for simple creating bot clients in discord API written in Python

Example client:
```
from disspy import Client

client = Client(token='your_token')

@client.event
async def ready():
    print("Hello! I'm ready!")

client()
```

This bot will print "Hello! I'm ready!" string in console when it become ready

More examples you can find in `examples` directory on this link:


### Links

GitHub repo: https://github.com/pixeldeee/disspy

More examples: https://github.com/pixeldeee/disspy/tree/master/examples

PyPi: https://pypi.org/project/disspy

Docs: https://disspy.readthedocs.io/en/latest
'''

from disspy.app import *
from disspy.channel import *
from disspy.client import *
from disspy.profiles import *
from disspy.ui import *

# Info
__version__: str = '1.0-alpha-1'
__lib_name__: str = 'disspy'
__lib_description__: str = (
    'Disspy is a library for simple creating bot clients in discord API written in Python'
)
