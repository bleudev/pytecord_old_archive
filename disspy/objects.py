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


__name__: str = "types"

__package__: str = "disspy"

__all__: list = [
    # Run types
    "DisBotStatus",
    # Event types
    "DisBotEventType"
]

_fall = __all__


class DisBotStatus:
    """
    Class for adding discord status for bot

    Examples
    bot.run(disspy.DisBotStatus.ONLINE)

    bot.run(disspy.DisBotStatus.DND)

    bot.run(disspy.DisBotStatus.IDLE)
    ---------------
    And you may use status in __init__()
    bot = disspy.DisBot(token="TOKEN", type="message",
                        status=disspy.DisBotStatus.ONLINE)
    """
    _numeral_of_class = 0

    _T = TypeVar(_fall[_numeral_of_class])

    ONLINE = "online"
    DND = "dnd"
    INVISIBLE = "invisible"
    IDLE = "idle"

    def __all__(self) -> list:
        """
        Returns all varibles in this class

        :return list: All varibles in this class
        """
        return [self.ONLINE, self.DND, self.INVISIBLE, self.IDLE]

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of this class

        :return type: Type of class
        """
        return self._T


class DisBotEventType:
    """
    This class created for simplification adding events to DisBot.
    This is class, not an object

    Using
    ------
    @bot.on(disspy.DisBotEventType.ONMESSAGEC)
    async def on_messagec(message):
        await message.channel.send('Test!')
    """

    _numeral_of_class = 1

    _T = TypeVar(_fall[_numeral_of_class])

    ON_MESSAGEC = "messagec"
    ON_READY = "ready"

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of this class

        :return type: Type of class
        """
        return self._T

    def __all__(self) -> list:
        """
        Returns all varibles in this class

        :return list: All varibles in this class
        """
        return [self.ON_READY, self.ON_MESSAGEC]

    def __str__(self) -> str:
        """
        It is using in str() method

        :return str: Default value of event (on_ready event)
        """
        return self.ON_READY
