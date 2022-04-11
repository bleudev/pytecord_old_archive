from dispy.https import Rest
from dispy import errs
from dispy.channel import DisChannel
from dispy.guild import DisGuild
from dispy.embed import DisEmbed
from dispy.message import DisMessage
from dispy.user import DisUser

from dispy.https import DisApi

from typing import *
__all__ = (
    "class DisBot"
)

System = {
    bool: bool
}


class DisBotType:
    __description__: str = "Class for using types for DisBot"  # Description to class

    __varibles__: dict[str, str] = {  # Description to varibles
        "SLASH": ":type: property, :returns: str - Will be called when integration is creating (slash command, context menu)",
        "MESSAGE": ":type: property, :returns: str - Will be called when message created",
        "COMMAND": ":type: property, :returns: str - Will be called when command called (for example, !help)"
    }

    # Mini doc with using
    __doc__: str = "Using:" \
                   "bot = dispy.DisBot(type=dispy.DisBotType.SLASH()) # Creating bot with slash commands and context menus"

    _T: TypeVar = TypeVar("DisBotType")

    _SLASH: str = "slash"
    _MESSAGE: str = "message"
    _COMMAND: str = "command"

    @property
    def __class__(self) -> TypeVar:
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

        self.status = status

        self._api = DisApi(token)

        self.isready = False

        if prefix == "" or " " in prefix:
            raise errs.BotPrefixError("Invalid prefix! Try another!")
        else:
            self.prefix = prefix

    async def _on_ready(self):
        return

    async def _on_messagec(self, message: DisMessage):
        return

    async def _register(self, d):
        # print(d)
        self.user: DisUser = self.get_user(d["user"]["id"], False)

    def on(self, type: str):
        """
        This method was created for changing on_ready and on_message method that using in runner

        :param type: Type of event
        :return: None (wrapper)
        """
        def wrapper(func):
            if type == "messagec":
                self._on_messagec = func
            elif type == "ready":
                self._on_ready = func
            else:
                raise errs.BotEventTypeError("Invalid type of event!")

        return wrapper

    def run(self, status: str):
        """
        Running bot

        :param status: Status for bot user
        :return: None
        """
        self.isready = True

        if status is None and self.status is None:
            self.status = "online"
        elif status is not None and self.status is None:
            self.status = status
        elif status is not None and self.status is not None:
            raise errs.BotStatusError("You typed status and in run() and in __init__()")

        self._runner(self.status, 10, 512)

    def _runner(self, status, version: int, intents: int):
        self._api.run(version, intents, status)

        return 0  # No errors

    async def send(self, channel_id: int, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embeds=embeds)
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

    def get_user(self, id: int, premium_gets: System[bool] = True):
        return DisUser(id, self._rest, premium_gets)
