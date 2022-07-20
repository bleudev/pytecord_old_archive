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

# Package imports
from asyncio import run
# Typing imports
from typing import (
    Optional,
    TypeVar,
    Union,
    Type,
    Callable,
    NoReturn,
    final,
    NewType,
    Generic
)

import requests.exceptions

# Disspy imports
from disspy import errors
from disspy._typing import (
    TypeOf,
    Event
)
from disspy.activity import *
from disspy.application_commands import *
from disspy.channel import *
from disspy.core import (
    DisApi,
    DisFlags,
    Showflake,
    ChannelId
)
from disspy.embed import DisEmbed
from disspy.guild import DisGuild
from disspy.jsongenerators import _OptionGenerator
from disspy.logger import Logger
from disspy.user import DisUser

__all__: tuple[str] = (
    "DisBot"
)

# For Type Hints
Wrapper = Callable

# Basics events
_all_basic_events = [
    "ready",  # On ready
    "messagec",  # On message create
    "messageu",  # On message update
    "messaged",  # On message delete
    "close",  # On closing bot
    "reaction",  # On reaction add
    "reactionr",  # On reaction remove
    "typing",  # Typing start
    "dm_typing"  # Typig start in dm channel
]


@final
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

    _T = TypeVar("DisBotStatus")

    ONLINE = "online"
    DND = "dnd"
    INVISIBLE = "invisible"
    IDLE = "idle"

    def __all__(self) -> list:
        """
        Returns all varibles in this class
        -----
        :return list: All varibles in this class
        """
        return [self.ONLINE, self.DND, self.INVISIBLE, self.IDLE]

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of this class
        -----
        :return type: Type of class
        """
        return self._T


@final
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

    _T = TypeVar("DisBotEventType")

    ON_MESSAGEC: str = "messagec"
    ON_MESSAGEU: str = "messageu"
    ON_MESSAGED: str = "messaged"
    ON_READY: str = "ready"
    ON_CLOSE: str = "close"
    ON_REACTION: str = "reaction"
    ON_REACTIONR: str = "reactionr"
    ON_TYPING: str = "typing"
    ON_DM_TYPING: str = "dm_typing"

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of this class
        -----
        :return type: Type of class
        """
        return self._T

    def __all__(self) -> list:
        """
        Returns all varibles in this class
        -----
        :return list: All varibles in this class
        """
        return [self.ON_READY, self.ON_MESSAGEC, self.ON_MESSAGEU, self.ON_MESSAGED,
                self.ON_CLOSE, self.ON_REACTION, self.ON_REACTIONR, self.ON_TYPING, self.ON_DM_TYPING]

    def __str__(self) -> str:
        """
        It is using in str() method
        -----
        :return str: Default value of event (on_ready event)
        """
        return self.ON_READY


class _BaseBot:
    """
    Class parent for DisBot
    """
    _T = TypeVar("_BaseBot")

    def __init__(self, token: Showflake[str]):
        """
        Create bot
        -----
        :param token: Discord Developers Portal Bot Token
        """
        self.token = token

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of this class
        -----
        :return TypeVar: Type of class
        """
        return self._T


@final
class DisBot(_BaseBot):
    """
    Class for accessing and sending information in Discord API
    -----
    :var token: Token for accessing and sending info
                (Token from Discord Developer Portal)
    :var application_id: Application id of bot
                         (from Discord Developer Portal)
    :var flags: Flags (Intents) for bot
    :var user: Bot User object
    """

    _T = TypeVar("DisBot")
    __parent__ = TypeVar("_BaseBot")
    __classname__ = "DisBot"

    def __init__(self, token: Showflake[str], application_id: Optional[Showflake[int]] = None,
                 status: Optional[TypeOf(DisBotStatus)] = None,
                 flags: Optional[TypeOf(DisFlags)] = None,
                 debug: Optional[bool] = False,
                 activity: Optional[Union[Activity, dict]] = None) -> NoReturn:
        """
        Create bot
        -----
        :param token: Discord Developers Portal Bot Token
        :param status: Status that use in run()
        :param flags: Flags (Intents) for bot (default is 512)
        """

        super().__init__(token)

        from requests import get

        _u = "https://discord.com/api/v10/users/@me"
        test_j = get(_u, headers={'Authorization': f'Bot {token}'}).json()

        try:
            if test_j["message"] == "401: Unauthorized" and test_j["code"] == 0:
                raise errors.Unauthorized()
        except KeyError:
            pass

        self.token: str = str(token)

        if flags is None:
            self.intflags = DisFlags.default()
        else:
            self.intflags = flags

        if activity is None:
            activity = {}

        if isinstance(activity, Activity):
            activity = activity.json()

        self._act = activity

        self.status = status
        self._debug = debug
        self._ons = {
            "ready": None,
            "messagec": None,
            "messageu": None,
            "messaged": None,
            "register": self._on_register,
            "register2": None,
            "interaction": None,
            "components": None,
            "modalsumbit": None,
            "reaction": None,
            "reactionr": None,
            "typing": None,
            "dm_typing": None,
            "channel": [None, 0]
        }

        self._on_messagec = None
        self._on_ready = None

        self.user = None

        if application_id is None or application_id == 0:
            application_id = 0
        else:
            from requests import get

            _u = f"https://discord.com/api/v10/applications/{application_id}/commands"
            test2_j = get(_u, headers={'Authorization': f'Bot {token}'}).json()

            try:
                if test2_j["message"] == "Unknown Application" and test2_j["code"] == 10002:
                    raise errors.BotApplicationIdInvalid("Invalid Application id!")
            except KeyError:
                pass
            except TypeError:
                pass

        self.api = DisApi(self.token, self.intflags, application_id)
        self.application_id = application_id

        self.isready = False

        self.logger = Logger()
        self.__classname__ = "DisBot"

        self.__slots__ = [self.api, self._on_ready, self._on_messagec,
                          self.token, self.user, self.isready, self.status]

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of this class
        -----
        :return TypeVar: Type of class
        """
        return self._T

    async def _on_register(self):
        """
        Register user var
        -----
        :return None:
        """
        self.user: DisUser = self.api.user

    def _on_close(self):
        pass

    def on(self, t: Event(DisBotEventType, str)) -> Wrapper:
        """
        This method was created for changing on_ready(), on_messagec()
        and other methods that using in _runner
        -----
        :param t: Type of event
        :return Wrapper:
        """

        __methodname__ = f"{self.__classname__}.on()"

        if isinstance(t, DisBotEventType):
            _message = f"Error! In method {__methodname__} was moved" \
                       "invalid argument! Argument type is DisBotEventType," \
                       "but in method have to type is str!"
            self.logger.log(_message)

        def wrapper(func):
            if t in _all_basic_events:
                if t == "close":
                    self._on_close = func
                else:
                    if t == "messagec" or t == "typing" or t == "dm_typing":
                        if self.intflags >= DisFlags.messages():
                            self._ons[t] = func
                        else:
                            raise errors.BotEventVisibleError(
                                "messagec(), typing() and dm_typing() events don't avaivable right now because flags < DisFlags.messages()")
                    elif t == "reaction" or t == "reactionr":
                        if self.intflags >= DisFlags.reactions():
                            self._ons[t] = func
                        else:
                            raise errors.BotEventVisibleError(
                                "reaction() and reactionr() evens don't avaivable right now because flags < DisFlags.reactions()")
                    else:
                        self._ons[t] = func
            else:
                _err = f"Error! In method {__methodname__} was" \
                       "moved invalid event type!"
                self.logger.log(_err)
                raise errors.BotEventTypeError("Invalid type of event!")

        return wrapper

    def add_event(self, t: Event(DisBotEventType, str), func: Callable) -> NoReturn:
        __methodname__ = f"{self.__classname__}.add_event()"

        if isinstance(t, DisBotEventType):
            _message = f"Error! In method {__methodname__} was moved" \
                       "invalid argument! Argument type is DisBotEventType," \
                       "but in method have to type is str!"
            self.logger.log(_message)

        if t in _all_basic_events:
            if t == "close":
                self._on_close = func
            else:
                self._ons[t] = func
        else:
            _err = f"Error! In method {__methodname__} was" \
                   "moved invalid event type!"
            self.logger.log(_err)
            raise errors.BotEventTypeError("Invalid type of event!")

    def on_message(self, t: str) -> Wrapper:
        """
        Method for changing on_message() events
        -----
        :param t: Type of on_message() event
        :return Wrapper:
        """
        _ts: list[str] = [
            "create",  # Message create
            "update",  # Message update
            "delete"  # Message delete
        ]

        _mse: list[str] = [
            "messagec",  # Message create
            "messageu",  # Message edit
            "messaged"  # Message delete
        ]

        def wrapper(func):
            if t in _ts:
                if t == _ts[0]:  # Message create
                    self._ons[_mse[0]] = func
                elif t == _ts[1]:  # Message update
                    self._ons[_mse[1]] = func
                elif t == _ts[2]:  # Message delete
                    self._ons[_mse[2]] = func

        return wrapper

    def on_channel(self, channel_id: ChannelId) -> Wrapper:
        def wrapper(func):
            self._ons["channel"] = [func, channel_id]

        return wrapper

    def slash_command(self, name, description, options: Optional[list[Option]] = None) -> Wrapper:
        """
        Create slash command
        -----
        :param name: Command's name
        :param description: Command's description
        :param options: Command's options
        :return Wrapper:
        """
        if self.application_id != 0:
            _payload = {}

            if options:
                _options_jsons = []

                for o in options:
                    _options_jsons.append(_OptionGenerator(o))

                _payload = {
                    "name": name,
                    "description": description,
                    "type": 1,
                    "options": _options_jsons
                }
            else:
                _payload = {
                    "name": name,
                    "description": description,
                    "type": ApplicationCommandType.TEXT_INPUT
                }

            def wrapper(func):
                self.api.create_command(_payload, func)

            return wrapper
        else:
            print("There is not application id")

    def add_slash_command(self, command: SlashCommand) -> NoReturn:
        """
        Create slash command
        -----
        :param command: Slash Command
        :return None:
        """
        if self.application_id != 0:
            _payload = {
                "name": command.name,
                "description": command.description,
                "type": ApplicationCommandType.TEXT_INPUT,
                "options": command.options
            }

            self.api.create_command(_payload, command.cmd)
        else:
            print("There is not application id")

    def user_command(self, name) -> Wrapper:
        """
        Create user command
        -----
        :param name: Command's name
        :return Wrapper:
        """
        if self.application_id != 0:
            _payload = {
                "name": name,
                "type": ApplicationCommandType.USER
            }

            def wrapper(func):
                self.api.create_command(_payload, func)

            return wrapper
        else:
            print("There is not application id")

    def add_user_command(self, command: UserCommand) -> NoReturn:
        """
        Create user command
        -----
        :param command: User Command
        :return None:
        """
        if self.application_id != 0:
            _payload = {
                "name": command.name,
                "type": ApplicationCommandType.USER,
            }

            self._api.create_command(_payload, command.cmd)
        else:
            print("There is not application id")

    def message_command(self, name) -> Wrapper:
        """
        Create message command
        -----
        :param name: Command's name
        :return Wrapper:
        """
        if self.application_id != 0:
            _payload = {
                "name": name,
                "type": ApplicationCommandType.MESSAGE
            }

            def wrapper(func):
                self.api.create_command(_payload, func)

            return wrapper
        else:
            print("There is not application id")

    def add_message_command(self, command: MessageCommand) -> NoReturn:
        """
        Create message command
        -----
        :param command: Message Command
        :return None:
        """
        if self.application_id != 0:
            _payload = {
                "name": command.name,
                "type": ApplicationCommandType.MESSAGE,
            }

            self.api.create_command(_payload, command.cmd)
        else:
            print("There is not application id")

    def run(self, status: Optional[Union[DisBotStatus, str]] = None) -> NoReturn:
        """
        Running bot
        -----
        :param status: Status for bot user
        :return: None
        """
        __methodname__ = f"{self.__classname__}.run()"

        if isinstance(status, DisBotStatus):
            _message = f"Error! In method {__methodname__} was moved " \
                       "invalid argument! Argument type is DisBotStatus, " \
                       "but in method have to type is str!"
            self.logger.log(_message)
            raise errors.InvalidArgument("Invalid argument type!")

        self.isready = True

        if status is None and self.status is None:
            self.status = "online"
        elif status is not None and self.status is None:
            self.status = status
        elif status is not None and self.status is not None:
            _message = "You typed status and in run() and in __init__()"
            raise errors.BotStatusError(_message)

        self._runner()

    def _runner(self) -> NoReturn:
        try:
            self._coro = run(self.api.run(self.status, self._ons, debug=self._debug, act=self._act))
        except KeyboardInterrupt:
            pass
        except requests.exceptions.ConnectionError:
            raise errors.InternetError("Please turn on your Wifi-Fi!", "-1000")

    async def disconnect(self) -> NoReturn:
        """
        Disconnect from Gateway
        -----
        :return asyncio.Future:
        """
        await self._dissconnenter()

    async def close(self) -> NoReturn:
        """
        Disconnect from Gateway
        :return asyncio.Future:
        """
        await self._dissconnenter()

    async def _dissconnenter(self) -> NoReturn:
        if self.isready:
            await self.api.disconnecter()

            for _var in self.__slots__:
                del _var

    async def send(self, channel_id: int, content: Optional[str] = None,
                   embeds: Optional[list[DisEmbed]] = None):
        """
        Send message to channel
        -----
        :param channel_id: Channel Id
        :param content: Message Content
        :param embeds: Message embeds
        :return None:
        """
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embeds=embeds)
        else:
            raise errors.InternetError("Bot is not ready!")

    async def send(self, channel_id: int, content: Optional[str] = None,
                   embed: Optional[DisEmbed] = None):
        """
        Send message to channel
        -----
        :param channel_id: Channel Id
        :param content: Message Content
        :param embed: Message embed
        :return None:
        """
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embed=embed)
        else:
            raise errors.InternetError("Bot is not ready!")

    def get_channel(self, id: ChannelId) -> DisChannel:
        """
        Get channel from id
        -----
        :param id: Channel Id
        :return DisChannel:
        """
        return self.api.get_channel(id)

    def get_guild(self, id: int) -> DisGuild:
        """
        Get guild from id
        -----
        :param id: Guild Id
        :return DisGuild:
        """
        return self.api.get_guild(id)

    def get_user(self, id: int) -> DisUser:
        """
        Get user from id
        -----
        :param id: User Id
        :return DisUser:
        """
        return self.api.get_user(id)

    async def change_activity(self, activity: Union[Activity, dict]):
        """
        Change activity
        -----
        :param activity: Activity to change
        :return None:
        """
        from datetime import datetime
        from time import mktime

        act = {}

        if isinstance(activity, Activity):
            act = activity.json()
        elif isinstance(activity, dict):
            act = activity

        await self.api.fsend_request({
            "op": 3,
            "d": {
                "since": mktime(datetime.now().timetuple()) * 1000,
                "afk": self.api.f.isafk,
                "status": self.status,
                "activities": [act]
            }
        })

        del datetime, mktime

    def __del__(self):
        self._on_close()
