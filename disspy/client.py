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
    Union,
    Callable,
    NoReturn,
    final,
    List
)

# Package imports
from enum import Enum, unique
from asyncio import run
from datetime import datetime
from time import mktime
from requests import get
import requests.exceptions


# Disspy imports
from disspy import errors
from disspy.typ import (
    TypeOf,
    Event
)
from disspy.activity import Activity
import disspy.application_commands as appc
from disspy.channel import (
    DisChannel,
    DisDmChannel
)
from disspy.core import (
    DisApi,
    DisFlags,
    Snowflake,
    ChannelId,
    ThreadId,
    GuildId,
    UserId
)
from disspy.embed import DisEmbed
from disspy.guild import DisGuild
from disspy.jsongenerators import _OptionGenerator
from disspy.user import DisUser
from disspy.thread import (
    DisNewsThread,
    DisThread,
    DisPrivateThread
)

__all__: tuple = (
    "DisBotStatus",
    "DisBotEventType",
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
    "dmessagec",  # On dm message create
    "dmessageu",  # On dm message update
    "dmessaged",  # On dm message delete
    "close",  # On closing bot
    "reaction",  # On reaction add
    "reactionr",  # On reaction remove
    "typing",  # Typing start
    "dm_typing"  # Typig start in dm channel
]


@final
class _BotLogger:
    pass


@final
@unique
class DisBotStatus(Enum):
    """
    Class for adding discord status for bot

    Examples
    bot.run(disspy.DisBotStatus.ONLINE)

    bot.run(disspy.DisBotStatus.DND)

    bot.run(disspy.DisBotStatus.IDLE)

    And you may use status in __init__()
    bot = disspy.DisBot(token="TOKEN", status=disspy.DisBotStatus.ONLINE)
    """

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

    def __str__(self) -> str:
        return "online"


@final
@unique
class DisBotEventType(Enum):
    """
    This class created for simplification adding events to DisBot.
    This is class, not an object

    Using
    ------
    @bot.on(disspy.DisBotEventType.ONMESSAGEC)
    async def on_messagec(message):
        await message.channel.send('Test!')
    """

    ON_MESSAGEC: str = "messagec"
    ON_MESSAGEU: str = "messageu"
    ON_MESSAGED: str = "messaged"
    ON_DMESSAGEC: str = "dmessagec"
    ON_DMESSAGEU: str = "dmessageu"
    ON_DMESSAGED: str = "dmessaged"
    ON_READY: str = "ready"
    ON_CLOSE: str = "close"
    ON_REACTION: str = "reaction"
    ON_REACTIONR: str = "reactionr"
    ON_TYPING: str = "typing"
    ON_DM_TYPING: str = "dm_typing"

    def __all__(self) -> list:
        """
        Returns all varibles in this class
        -----
        :return list: All varibles in this class
        """
        return [self.ON_READY, self.ON_MESSAGEC, self.ON_MESSAGEU,
                self.ON_MESSAGED, self.ON_DMESSAGEC, self.ON_DMESSAGEU,
                self.ON_DMESSAGED, self.ON_CLOSE, self.ON_REACTION,
                self.ON_REACTIONR, self.ON_TYPING, self.ON_DM_TYPING]

    def __str__(self) -> str:
        return "ready"


@final
class DisBot:
    """
    Class for accessing and sending information in Discord API
    """

    __classname__ = "DisBot"

    def __init__(self, token: Snowflake[str], status: Optional[TypeOf(DisBotStatus)] = None,
                flags: Optional[TypeOf(DisFlags)] = None, debug: Optional[bool] = False,
                activity: Optional[Union[Activity, dict]] = None) -> NoReturn:
        """
        Create bot
        -----
        :param token: Discord Developers Portal Bot Token
        :param status: Status that use in run()
        :param flags: Flags (Intents) for bot (default is 512)
        """

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
            "dmessagec": None,
            "dmessageu": None,
            "dmessaged": None,
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

        self.api = DisApi(self.token, self.intflags)

        self.isready = False

        self.__classname__ = "DisBot"

        self.__slots__ = [self.api, self._on_ready, self._on_messagec,
                            self.token, self.user, self.isready, self.status]

    async def _on_register(self):
        """
        Register user var
        -----
        :return None:
        """
        self.user: DisUser = self.api.user

    def _on_close(self):
        pass

    def on(self, event_type: Event(DisBotEventType, str)) -> Wrapper:
        """
        This method was created for changing on_ready(), on_messagec()
        and other methods that using in _runner
        -----
        :param t: Type of event
        :return Wrapper:
        """

        __methodname__ = f"{self.__classname__}.on()"

        if isinstance(event_type, DisBotEventType):
            _message = f"Error! In method {__methodname__} was moved" \
                        "invalid argument! Argument type is DisBotEventType," \
                        "but in method have to type is str!"
            raise errors.InvalidArgument(_message)

        def wrapper(func):
            if event_type in _all_basic_events:
                if event_type == "close":
                    self._on_close = func
                else:
                    if event_type in ["messagec", "messageu", "messaged", "typing", "dm_typing",
                                "dmessagec", "dmessageu", "dmessaged"]:
                        if self.intflags >= DisFlags.messages():
                            self._ons[event_type] = func
                        else:
                            raise errors.BotEventVisibleError(
                                "messagec(), typing(), dm_typing() and other events" +
                                "don't avaivable right now because flags < DisFlags.messages()")
                    elif event_type in ["reaction", "reactionr"]:
                        if self.intflags >= DisFlags.reactions():
                            self._ons[event_type] = func
                        else:
                            raise errors.BotEventVisibleError(
                                "reaction() and reactionr() events don't" +
                                " avaivable right now because flags < DisFlags.reactions()")
                    else:
                        self._ons[event_type] = func
            else:
                raise errors.BotEventTypeError("Invalid type of event!")

        return wrapper

    def add_event(self, event_type: Event(DisBotEventType, str), func: Callable) -> NoReturn:
        """
        Add event to bot with function and event type
        -----
        :param t: Type of Event
        :param func: Function
        :return None:
        """
        __methodname__ = f"{self.__classname__}.add_event()"

        if isinstance(event_type, DisBotEventType):
            _message = f"Error! In method {__methodname__} was moved" \
                        "invalid argument! Argument type is DisBotEventType," \
                        "but in method have to type is str!"
            raise errors.InvalidArgument(_message)

        if event_type in _all_basic_events:
            if event_type == "close":
                self._on_close = func
            else:
                self._ons[event_type] = func
        else:
            raise errors.BotEventTypeError("Invalid type of event!")

    def on_ready(self) -> Wrapper:
        """on_ready
        Method for changing on_ready() event

        Returns:
            Wrapper: function named wrapper
        """

        def wrapper(func):
            self._ons["ready"] = func

        return wrapper

    def on_message(self, event_type: str) -> Wrapper:
        """
        Method for changing on_message() events
        -----
        :param t: Type of on_message() event
        :return Wrapper:
        """
        _ts: List[str] = [
            "create",  # Message create
            "update",  # Message update
            "delete"  # Message delete
        ]

        _mse: List[str] = [
            "messagec",  # Message create
            "messageu",  # Message update
            "messaged"  # Message delete
        ]

        def wrapper(func):
            if event_type in _ts:
                if event_type == _ts[0]:  # Message create
                    self._ons[_mse[0]] = func
                elif event_type == _ts[1]:  # Message update
                    self._ons[_mse[1]] = func
                elif event_type == _ts[2]:  # Message delete
                    self._ons[_mse[2]] = func

        return wrapper

    def on_dm_message(self, event_type: str) -> Wrapper:
        """
        Method for changing on_dm_message() events
        -----
        :param t: Type of on_dm_message() event
        :return Wrapper:
        """
        _ts: List[str] = [
            "create",  # Message create
            "update",  # Message update
            "delete"  # Message delete
        ]

        _mse: List[str] = [
            "dmessagec",  # Message create
            "dmessageu",  # Message update
            "dmessaged"  # Message delete
        ]

        def wrapper(func):
            if event_type in _ts:
                if event_type == _ts[0]:  # Message create
                    self._ons[_mse[0]] = func
                elif event_type == _ts[1]:  # Message update
                    self._ons[_mse[1]] = func
                elif event_type == _ts[2]:  # Message delete
                    self._ons[_mse[2]] = func

        return wrapper

    def on_channel(self, channel_id: ChannelId) -> Wrapper:
        """
        On channel event (on_messagec event only in the channel)
        -----
        :param channel_id: Channel id
        :return Wrapper:
        """
        def wrapper(func):
            self._ons["channel"] = [func, channel_id]

        return wrapper

    def slash_command(self, name: str, description: str,
                      options: Optional[List[appc.Option]] = None) -> Wrapper:
        """
        Create slash command
        -----
        :param name: Command's name
        :param description: Command's description
        :param options: Command's options
        :return Wrapper:
        """
        _payload = {}

        if options:
            _options_jsons = []

            for option in options:
                _options_jsons.append(_OptionGenerator(option))

            _payload = {
                "name": name,
                "description": description,
                "type": appc.ApplicationCommandType.TEXT_INPUT,
                "options": _options_jsons
            }
        else:
            _payload = {
                "name": name,
                "description": description,
                "type": appc.ApplicationCommandType.TEXT_INPUT
            }

        def wrapper(func):
            self.api.create_command(_payload, func)

        return wrapper

    def add_slash_command(self, command: appc.SlashCommand) -> NoReturn:
        """
        Create slash command
        -----
        :param command: Slash Command
        :return None:
        """
        self.api.create_command(command.json(), command.cmd)

        return None

    def user_command(self, name: str) -> Wrapper:
        """
        Create user command
        -----
        :param name: Command's name
        :return Wrapper:
        """
        _payload = {
            "name": name,
            "type": appc.ApplicationCommandType.USER
        }

        def wrapper(func):
            self.api.create_command(_payload, func)

        return wrapper

    def add_user_command(self, command: appc.UserCommand) -> NoReturn:
        """
        Create user command
        -----
        :param command: User Command
        :return None:
        """
        self.api.create_command(command.json(), command.cmd)

        return None

    def message_command(self, name: str) -> Wrapper:
        """
        Create message command
        -----
        :param name: Command's name
        :return Wrapper:
        """
        _payload = {
            "name": name,
            "type": appc.ApplicationCommandType.MESSAGE
        }

        def wrapper(func):
            self.api.create_command(_payload, func)

        return wrapper

    def add_message_command(self,
                            command: appc.MessageCommand) -> NoReturn:
        """
        Create message command
        -----
        :param command: Message Command
        :return None:
        """
        self.api.create_command(command.json(), command.cmd)

        return None

    def add_application_command(self, command: appc.ApplicationCommand) -> NoReturn:
        """
        Create application command
        -----
        :param command: Application Command
        :return None:
        """
        self.api.create_command(command.json(), command.cmd)

        return None

    def run(self, status: Optional[Union[DisBotStatus, str]] = None,
            activity: Optional[Union[Activity, dict]] = None) -> NoReturn:
        """
        Running bot
        -----
        :param status: Status for bot user
        :return: None
        """
        if isinstance(status, DisBotStatus):
            raise errors.InvalidArgument("Invalid argument type!")

        self.isready = True

        if status:
            self.status = status
        elif not status and not self.status:
            self.status = "online"

        if activity:
            self._act = activity

        self._runner()

    def _runner(self) -> NoReturn:
        try:
            run(self.api.run(self.status, self._ons,
                                debug=self._debug, act=self._act))
        except KeyboardInterrupt:
            pass
        except requests.exceptions.ConnectionError:
            raise errors.InternetError("Please turn on your internet!", "-1000")

    async def disconnect(self) -> NoReturn:
        """
        Disconnect from Gateway
        """
        await self._dissconnenter()

    async def close(self) -> NoReturn:
        """
        Disconnect from Gateway
        """
        await self._dissconnenter()

    async def _dissconnenter(self) -> NoReturn:
        if self.isready:
            await self.api.disconnecter()

            for _var in self.__slots__:
                del _var

    async def send(self, channel_id: int, content: Optional[str] = None,
                    embeds: Optional[List[DisEmbed]] = None):
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

    def get_channel(self, channel_id: ChannelId) -> Union[DisChannel, DisDmChannel]:
        """
        Get channel from id
        -----
        :param channel_id: Channel Id
        :return Union[DisChannel, DisDmChannel]:
        """
        _u = f"https://discord.com/api/v10/channels/{channel_id}"
        _hdrs = {'Authorization': f'Bot {self.token}'}

        j = get(_u, headers=_hdrs).json()

        if j["type"] == 1:  # Dm Channels
            return DisDmChannel(channel_id, self.token)

        return DisChannel(channel_id, self.token)

    def get_thread(self, thread_id: ThreadId):
        """get_thread
        Get thread by id

        Args:
            thread_id (ThreadId): Thread id

        Raises:
            RuntimeError: Argument is not thread id

        Returns:
            Union[DisNewsThread, DisThread, DisPrivateThread]: Getted thread object
        """
        _u = f"https://discord.com/api/v10/channels/{thread_id}"
        _hdrs = {'Authorization': f'Bot {self.token}',
                 'content-type': 'application/json'}

        j = get(_u, headers=_hdrs).json()

        if j["type"] == 10:  # News thread
            return DisNewsThread(j, self.token)

        if j["type"] == 11:  # Public thread
            return DisThread(j, self.token)

        if j["type"] == 12:  # Private thread
            return DisPrivateThread(j, self.token)

        raise RuntimeError("This channel is not thread! Use get_channel() method")

    def get_guild(self, guild_id: GuildId) -> DisGuild:
        """
        Get guild from id
        -----
        :param guild_id: Guild Id
        :return DisGuild:
        """
        return self.api.get_guild(guild_id)

    def get_user(self, user_id: UserId) -> DisUser:
        """
        Get user from id
        -----
        :param user_id: User Id
        :return DisUser:
        """
        return self.api.get_user(user_id)

    async def change_activity(self, activity: Union[Activity, dict]):
        """
        Change activity
        -----
        :param activity: Activity to change
        :return None:
        """
        act = {}

        if isinstance(activity, Activity):
            act = activity.json()
        elif isinstance(activity, dict):
            act = activity

        await self.api.fsend_request({
            "op": 3,
            "d": {
                "since": mktime(datetime.now().timetuple()) * 1000,
                "afk": self.api.flow.isafk,
                "status": self.status,
                "activities": [act]
            }
        })

    def __del__(self):
        self._on_close()
