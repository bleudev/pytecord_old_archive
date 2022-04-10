from dispy.http.rest import Rest
import dispy.errs as errs

from .channel import DisChannel
from . import DisBotType
from .guild import DisGuild
from .embed import DisEmbed
from .message import DisMessage
from typing import *
from .http.gateway import Gateway

__all__ = (
    "class DisBot"
)


class _BaseBot:
    _SLASH: str = "slash"
    _MESSAGE: str = "message"
    _COMMAND: str = "command"

    _isslash = False
    _ismessage = False
    _iscommand = False

    _NUMS = {
        "slash": 1,
        "message": 2,
        "command": 3
    }

    def __init__(self, token: str, type: str, prefix: Optional[str] = "!"):
        self.token = token
        self.type = type

        self.commands = {}
        """
            For example:
            self.commands = {
                "help": help()
            }
        """

        try:
            _type_num = self._NUMS[type]

            if _type_num == 1:
                self._isslash = True
            elif _type_num == 2:
                self._ismessage = True
            elif _type_num == 3:
                self._iscommand = True
        except KeyError:
            raise errs.BotTypeError("Invalid type! Try again!")

        self.prefix = prefix

    if _iscommand:
        async def command(self, name: str):
            def wrapper(func):
                self.commands[name] = func
            return wrapper


class DisBotStatus:
    ONLINE = "online"
    DND = "dnd"
    INVISIBLE = "invisible"
    IDLE = "idle"


class DisBot(_BaseBot):
    def __init__(self, token: str, type: Union[DisBotType, str], prefix: Optional[str] = "!", status: Optional[str] = None):
        """
        Create bot

        :param token: Discord Developers Portal Bot Token
        :param prefix: Prefix for bot (There is no spaces!)
        """

        super().__init__(token, type, prefix)

        self._rest = Rest(token)

        self.status = status

        self.isready = False
        if prefix == "" or " " in prefix:
            raise errs.BotPrefixError("Invalid prefix! Try another!")
        else:
            self.prefix = prefix

    async def on_ready(self):
        return

    def on_message(self, message: DisMessage):
        return

    def on(self, type: str):
        """
        This method was created for changing on_ready and on_message method that using in runner

        :param type: Type of event
        :return: None (wrapper)
        """
        def wrapper(func):
            if type == "messagec":
                self.on_message = func
            elif type == "ready":
                self.on_ready = func
            else:
                print("Error in on() - Invalid type of event (read docs)")

        return wrapper

    def run(self, status: Optional[Union[DisBotStatus, str]] = None):
        """
        Running bot

        :param status: Status for bot user
        :return: None
        """
        self.isready = True

        if self.status is None or status is None:
            self.status = "online"

        elif status is not None:
            self.status = status

        self._runner(self.status, 10, 512)

    def _runner(self, status: str, version: int, intents: int):
        Gateway(version, self._rest.token, intents, {}, status, self.on_ready, self.on_message)

        return 0  # No errors

    async def send(self, channel_id: int, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embeds=embeds)
            return DisMessage(self._rest.fetch(channel.id), self._rest)
        else:
            raise errs.InternetError("Bot is not ready!")

    async def send(self, channel_id: int, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embed=embed)
            return DisMessage(self._rest.fetch(channel.id), self._rest)
        else:
            raise errs.InternetError("Bot is not ready!")

    def get_channel(self, id: int):
        return DisChannel(self._rest.get('channel', id), self._rest)

    def get_guild(self, id: int):
        return DisGuild(self._rest.get('guild', id), self._rest)
