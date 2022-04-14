"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .client import DisBot, DisBotStatus, DisBotType
from .errs import UserNitroTypeError, InternetError, BotTypeError, BotPrefixError, MissingPerms
from .guild import DisGuild
from .channel import DisChannel
from .embed import DisEmbed, DisField, DisColor
from .message import DisMessage
from .user import DisUser
from .core import DisApi, DisFlags

import typing

"""
    Main information about dispy
    
    :var: __version__ -> Version of dipsy
    :var: __github__ -> Link to github repo
    :var: __packagename__ -> Name of package 
"""

__version__ = "0.1dev"
__minpythonver__ = "3.6"
__github__ = "https://github.com/itttgg/dispy"
__stablever__ = "https://github.com/itttgg/dispy/releases/tag/0.1a2"
__description__ = "Dispy - package for creating bots."
__packagename__ = "dispy"


class _DocObject:
    __description__: str = ""  # Description to class
    __doc__: str = ""  # Mini doc with using
    __varibles__: dict[str, str] = {}  # Description to varibles

    _T: typing.TypeVar = None

    def __str__(self) -> str:  # Using in str()
        r = ""

        for i in self.__varibles__.keys():
            if r == "":
                r += i
            else:
                r += f", {i}"

        return r


# Types for simpler creating bots
class DisBotEventType(_DocObject):  # Event type for DisBot
    __description__: str = "This class created for simplification adding events to DisBot. This is class, not an object"  # Description to class

    __varibles__: dict[str, str] = {  # Description to varibles
        "ON_MESSAGE": ":type: property, :returns: str - Will be called when new message was created in DisBot.guild.channel",
        "ON_READY": ":type: property, :returns: str - Will be called when bot becomes ready"
    }

    # Mini doc with using
    __doc__: str = "Using:" \
                   "@bot.on(dispy.DisBotEventType.ONMESSAGEC())" \
                   "async def on_messagec(message):" \
                   "    await message.channel.send('Test!')"

    _T: typing.TypeVar = typing.TypeVar("DisBotEventType")

    @property
    def __class__(self) -> typing.Type[_T]:
        return self._T

    @staticmethod
    def ON_MESSAGEC() -> str:
        return "messagec"

    @staticmethod
    def ON_READY() -> str:
        return "ready"
