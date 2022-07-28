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
    Type,
    Callable,
    NoReturn,
    final
)

# Package imports
from asyncio import run
from datetime import datetime
from time import mktime
from requests import get
import requests.exceptions


# Disspy imports
from disspy import errors
from disspy._typing import (
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
    Showflake,
    ChannelId
)
from disspy.embed import DisEmbed
from disspy.guild import DisGuild
from disspy.jsongenerators import _OptionGenerator
from disspy.logger import Logger
from disspy.user import DisUser

__all__: tuple[str] = (
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
class DisBotStatus:
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

    ON_MESSAGEC: str = "messagec"
    ON_MESSAGEU: str = "messageu"
    ON_MESSAGED: str = "messaged"
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
                self.ON_MESSAGED, self.ON_CLOSE, self.ON_REACTION,
                self.ON_REACTIONR, self.ON_TYPING, self.ON_DM_TYPING]

    def __str__(self) -> str:
        """
        It is using in str() method
        -----
        :return str: Default value of event (on_ready event)
        """
        return self.ON_READY


@final
class DisBot:
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

    try:
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

            if application_id is None or application_id == 0:
                application_id = 0
            else:
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
            self.application_id: int = int(application_id)

            self.isready = False

            self.logger = Logger()
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
                self.logger.log(_message)

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
                    _err = f"Error! In method {__methodname__} was" \
                           "moved invalid event type!"
                    self.logger.log(_err)
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
                self.logger.log(_message)

            if event_type in _all_basic_events:
                if event_type == "close":
                    self._on_close = func
                else:
                    self._ons[event_type] = func
            else:
                _err = f"Error! In method {__methodname__} was" \
                       "moved invalid event type!"
                self.logger.log(_err)
                raise errors.BotEventTypeError("Invalid type of event!")

        def on_message(self, event_type: str) -> Wrapper:
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
            _ts: list[str] = [
                "create",  # Message create
                "update",  # Message update
                "delete"  # Message delete
            ]

            _mse: list[str] = [
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
                          options: Optional[list[appc.Option]]
                          = None) -> Union[Wrapper, None]:
            """
            Create slash command
            -----
            :param name: Command's name
            :param description: Command's description
            :param options: Command's options
            :return Wrapper:
            """
            if self.application_id != 0 or self.application_id:
                _payload = {}

                if options:
                    _options_jsons = []

                    for option in options:
                        _options_jsons.append(_OptionGenerator(option))

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
                        "type": appc.ApplicationCommandType.TEXT_INPUT
                    }

                def wrapper(func):
                    self.api.create_command(_payload, func)

                return wrapper

            raise errors.ApplicationIdIsNone("Application commands is blocked")

        def add_slash_command(self, command: appc.SlashCommand) -> NoReturn:
            """
            Create slash command
            -----
            :param command: Slash Command
            :return None:
            """
            if self.application_id != 0 or self.application_id:
                _payload = {
                    "name": command.name,
                    "description": command.description,
                    "type": appc.ApplicationCommandType.TEXT_INPUT,
                    "options": command.options
                }

                self.api.create_command(_payload, command.cmd)

                return None

            raise errors.ApplicationIdIsNone("Application commands is blocked")

        def user_command(self, name) -> Union[Wrapper, None]:
            """
            Create user command
            -----
            :param name: Command's name
            :return Wrapper:
            """
            if self.application_id != 0 or self.application_id:
                _payload = {
                    "name": name,
                    "type": appc.ApplicationCommandType.USER
                }

                def wrapper(func):
                    self.api.create_command(_payload, func)

                return wrapper

            raise errors.ApplicationIdIsNone("Application commands is blocked")

        def add_user_command(self, command: appc.UserCommand) -> NoReturn:
            """
            Create user command
            -----
            :param command: User Command
            :return None:
            """
            if self.application_id != 0 or self.application_id:
                _payload = {
                    "name": command.name,
                    "type": appc.ApplicationCommandType.USER,
                }

                self.api.create_command(_payload, command.cmd)

                return None

            raise errors.ApplicationIdIsNone("Application commands is blocked")

        def message_command(self, name) -> Union[Wrapper, None]:
            """
            Create message command
            -----
            :param name: Command's name
            :return Wrapper:
            """
            if self.application_id != 0 or self.application_id:
                _payload = {
                    "name": name,
                    "type": appc.ApplicationCommandType.MESSAGE
                }

                def wrapper(func):
                    self.api.create_command(_payload, func)

                return wrapper

            raise errors.ApplicationIdIsNone("Application commands is blocked")

        def add_message_command(self,
                                command: appc.MessageCommand) -> NoReturn:
            """
            Create message command
            -----
            :param command: Message Command
            :return None:
            """
            if self.application_id != 0 or self.application_id:
                _payload = {
                    "name": command.name,
                    "type": appc.ApplicationCommandType.MESSAGE,
                }

                self.api.create_command(_payload, command.cmd)

                return None

            raise errors.ApplicationIdIsNone("Application commands is blocked")

        def run(self, status: Optional[Union[DisBotStatus, str]] = None, activity: Optional[Union[Activity, dict]] = None) -> NoReturn:
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

        def get_channel(self, channel_id: ChannelId) -> Union[DisChannel, DisDmChannel]:
            """
            Get channel from id
            -----
            :param channel_id: Channel Id
            :return Union[DisChannel, DisDmChannel]:
            """
            _u = f"https://discord.com/v10/channels/{channel_id}"
            _hdrs = {'Authorization': f'Bot {self.token}'}

            j = get(_u, headers=_hdrs).json()

            if j["type"] == 1:  # Dm Channels
                return DisDmChannel(channel_id, self.token)

            return DisChannel(channel_id, self.token)

        def get_guild(self, guild_id: int) -> DisGuild:
            """
            Get guild from id
            -----
            :param guild_id: Guild Id
            :return DisGuild:
            """
            return self.api.get_guild(guild_id)

        def get_user(self, user_id: int) -> DisUser:
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
                    "afk": self.api.f.isafk,
                    "status": self.status,
                    "activities": [act]
                }
            })

        def __del__(self):
            self._on_close()

    except errors.DisRunTimeError as exc:
        print(exc.__message__)
