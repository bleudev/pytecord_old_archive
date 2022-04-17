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

from typing import (
    Type,
    TypeVar
)


class DisBotStatus:
    """
        Hel class for adding discord staus for bot

        Examples
        bot.run(disspy.DisBotStatus.ONLINE)

        bot.run(disspy.DisBotStatus.DND)

        bot.run(disspy.DisBotStatus.IDLE)
        ---------------
        And you may use status in __init__()
        bot = disspy.DisBot(token="TOKEN", type="message", status=disspy.DisBotStatus.ONLINE)
    """
    _T = TypeVar("DisBotStatus")

    ONLINE = "online"
    DND = "dnd"
    INVISIBLE = "invisible"
    IDLE = "idle"

    @property
    def __class__(self) -> Type[_T]:
        """
            Returns type of this class
            --------
            :return self._T (Type of class):
        """
        return self._T


class DisBotEventType:  # Event type for DisBot
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

    _T: TypeVar = TypeVar("DisBotEventType")

    @property
    def __class__(self) -> Type[_T]:
        return self._T

    @staticmethod
    def ON_MESSAGEC() -> str:
        return "messagec"

    @staticmethod
    def ON_READY() -> str:
        return "ready"