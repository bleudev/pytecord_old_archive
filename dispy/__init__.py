from .client import DisBot, DisBotStatus
from .errs import *
from .guild import DisGuild
from .channel import DisChannel
from .embed import DisEmbed, DisField, DisColor
from .message import DisMessage
from .user import DisUser
import typing

"""
    Main information about dispy
    
    :var: __version__ -> Version of dipsy
    :var: __github__ -> Link to github repo
    :var: __packagename__ -> Name of package 
"""

__version__ = "0.2"
__github__ = "https://github.com/itttgg/dispy"
__package__ = "dispy"


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

    _ON_MESSAGEC: str = "messagec"
    _ON_READY: str = "ready"

    @property
    def __class__(self) -> typing.Type[_T]:
        return self._T

    @property
    def ON_MESSAGEC(self) -> str:
        return self._ON_MESSAGEC

    @property
    def ON_READY(self) -> str:
        return self._ON_READY


class DisBotType(_DocObject):
    __description__: str = "Class for using types for DisBot"  # Description to class

    __varibles__: dict[str, str] = {  # Description to varibles
        "SLASH": ":type: property, :returns: str - Will be called when integration is creating (slash command, context menu)",
        "MESSAGE": ":type: property, :returns: str - Will be called when message created",
        "COMMAND": ":type: property, :returns: str - Will be called when command called (for example, !help)"
    }

    # Mini doc with using
    __doc__: str = "Using:" \
                   "bot = dispy.DisBot(type=dispy.DisBotType.SLASH()) # Creating bot with slash commands and context menus"

    _T: typing.TypeVar = typing.TypeVar("DisBotType")

    _SLASH: str = "slash"
    _MESSAGE: str = "message"
    _COMMAND: str = "command"

    @property
    def __class__(self) -> typing.TypeVar:
        return self._T

    @property
    def SLASH(self) -> str:
        return self._SLASH

    @property
    def MESSAGE(self) -> str:
        return self._MESSAGE

    @property
    def COMMAND(self) -> str:
        return self._COMMAND
