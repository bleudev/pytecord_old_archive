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

# Typing imports
from typing import (
    Optional,
    TypeVar,
    Union,
    Type
)

# Package imports
from disspy import errs
from disspy.core import DisApi, DisFlags
from disspy.channel import DisChannel
from disspy.embed import DisEmbed
from disspy.guild import DisGuild
from disspy.user import DisUser
from disspy.objects import DisBotStatus, DisBotEventType
from disspy.logger import Logger
from disspy._typing import TypeOf

System = {
    bool: bool
}


class _BaseBot:
    _T = TypeVar("_BaseBot")

    def __init__(self, token: str):
        self.token = token

    @property
    def __class__(self) -> Type[_T]:
        """
            Returns type of this class
            --------
            :return self._T (Type of class):
        """
        return self._T


class DisBot(_BaseBot):
    """
    Class for accessing and sending information in Discord

    Attributes:
        :var token: Token for accessing and sending info
                    (Token from Discord Developer Portal).
        :var flags: Flags (Intents) for bot.
    """
    _T = TypeVar("DisBot")
    __parent__ = TypeVar("_BaseBot")
    __classname__ = "DisBot"

    def __init__(self, token: str, application_id: int,
                 status: Optional[TypeOf(DisBotStatus)] = None,
                 flags: Optional[TypeOf(DisFlags)] = None,
                 debug: Optional[bool] = False):
        """
        Create bot

        :param token: Discord Developers Portal Bot Token
        :param status: Status that use in run()
        :param flags: Flags (Intents) for bot (default is 512)
        """

        super().__init__(token)

        if flags is None:
            self.intflags = DisFlags.default()
        else:
            self.intflags = flags

        self.status = status
        self._debug = debug
        self._ons = {
            "ready": None,
            "messagec": None,
            "register": self._on_register,
            "register2": None,
            "interaction": None
        }

        self._on_messagec = None
        self._on_ready = None

        self.user = None

        self._api = DisApi(self.token, self.intflags, application_id)
        self.application_id = application_id

        self.isready = False

        self.logger = Logger()
        self.__classname__ = "DisBot"

        self.__slots__ = [self._api, self._on_ready, self._on_messagec,
                          self.token, self.user, self.isready, self.status]

    @property
    def __class__(self) -> Type[_T]:
        """
            Returns type of this class
            --------
            :return self._T (Type of class):
        """
        return self._T

    async def _on_register(self):
        pass
        # self.user: DisUser = self._api.user

    def on(self, type: Union[DisBotEventType, str]):
        """
        This method was created for changing on_ready and on_messagec
        method that using in runner

        :param type: Type of event
        :return: None (wrapper)
        """

        __methodname__ = f"{self.__classname__}.on()"

        if isinstance(type, DisBotEventType):
            _message = f"Error! In method {__methodname__} was moved" \
                       "invalid argument! Argument type is DisBotEventType," \
                       "but in method have to type is str!"
            self.logger.log(_message)

        def wrapper(func):
            if type == "messagec" or type == "ready":
                self._ons[type] = func
            else:
                _err = f"Error! In method {__methodname__} was" \
                       "moved invalid event type!"
                self.logger.log(_err)
                raise errs.BotEventTypeError("Invalid type of event!")

        return wrapper

    def slash_command(self, name, description):
        _payload = {
            "name": name,
            "description": description,
            "type": 1
        }

        def wrapper(func):
            self._api.create_command(_payload, func)

        return wrapper

    def user_command(self, name):
        _payload = {
            "name": name,
            "type": 2
        }

        def wrapper(func):
            self._api.create_command(_payload, func)

        return wrapper

    def message_command(self, name):
        _payload = {
            "name": name,
            "type": 3
        }

        def wrapper(func):
            self._api.create_command(_payload, func)

        return wrapper

    def run(self, status: Union[DisBotStatus, str] = None) -> int:
        """
        Running bot

        :param status: Status for bot user
        :return: None
        """
        __methodname__ = f"{self.__classname__}.on()"

        if isinstance(status, DisBotStatus):
            _message = f"Error! In method {__methodname__} was moved " \
                       "invalid argument! Argument type is DisBotStatus, " \
                       "but in method have to type is str!"
            self.logger.log(_message)
            raise errs.InvalidArgument("Invalid argument type!")

        self.isready = True

        if status is None and self.status is None:
            self.status = "online"
        elif status is not None and self.status is None:
            self.status = status
        elif status is not None and self.status is not None:
            _message = "You typed status and in run() and in __init__()"
            raise errs.BotStatusError(_message)

        _err = self._runner()

        if not _err == 0:
            raise RuntimeError(f"{_err} | Error!")

        return _err

    def _runner(self) -> int:
        from asyncio import run

        self._coro = run(self._api.run(self.status, self._ons, debug=self._debug))

        return 0  # No errors

    def disconnect(self) -> int:
        return self._dissconnenter()

    def close(self) -> int:
        return self._dissconnenter()

    def _dissconnenter(self) -> int:
        if self.isready:
            for _var in self.__slots__:
                del _var

            return 0
        else:
            return -99

    async def send(self, channel_id: int, content: Optional[str] = None,
                   embeds: Optional[list[DisEmbed]] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embeds=embeds)
        else:
            raise errs.InternetError("Bot is not ready!")

    async def send(self, channel_id: int, content: Optional[str] = None,
                   embed: Optional[DisEmbed] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embed=embed)
        else:
            raise errs.InternetError("Bot is not ready!")

    def get_channel(self, id: int) -> DisChannel:
        return self._api.get_channel(id)

    def get_guild(self, id: int) -> DisGuild:
        return self._api.get_guild(id)

    def get_user(self, id: int, premium_gets: System[bool] = True) -> DisUser:
        return self._api.get_user(id, premium_gets)
