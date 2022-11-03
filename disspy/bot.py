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
from typing import Optional, Union, Callable, final, List, Literal

# Package imports
from pathlib import Path
from asyncio import run
from datetime import datetime
from time import mktime
import os
from inspect import signature
from requests import get
import requests.exceptions

# Disspy imports
from disspy import errors
from disspy.typ import TypeOf, MISSING
from disspy.activity import Activity
import disspy.app_commands as appc
from disspy.channel import DisChannel, DisDmChannel, DisMessage, DmMessage
from disspy.http import DisApi, DisFlags
from disspy.guild import Guild
from disspy.user import DisUser
from disspy.thread import DisNewsThread, DisThread, DisPrivateThread
from disspy.abstract import Channel, Message, Thread
from disspy.state import ConnectionState
from disspy.application import Application
from disspy.utils import _type_check, _type_of, optional, type_check_obj

__all__: tuple = ("DisBotEventType", "Client")

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
    "dm_typing",  # Typig start in dm channel
]


#####################
# For code readable #
#####################


async def blank():
    """Blank method"""
    return


def ignore():
    """Ignore"""
    return


@final
class _BotLogger:
    def __init__(self) -> None:
        self.logs = []

    def log(self, msg: str):
        """log
        Log to Logger

        Args:
            msg (str): Message
        """
        _datetime = datetime.now()

        tformat = "%d/%d/%d %d:%d:%d"

        _time = tformat % (
            _datetime.year,
            _datetime.month,
            _datetime.day,
            _datetime.hour,
            _datetime.minute,
            _datetime.second,
        )

        self.logs.append(f"[{_time}] {msg}")


@final
class DisBotEventType:
    """
    This class created for simplification adding events to Client.
    This is class, not an object

    Using
    ------
    @bot.on(disspy.DisBotEventType.ONMESSAGEC)
    async def on_messagec(message):
        await message.channel.send('Test!')
    """

    MESSAGEC: str = "messagec"
    MESSAGEU: str = "messageu"
    MESSAGED: str = "messaged"
    DMESSAGEC: str = "dmessagec"
    DMESSAGEU: str = "dmessageu"
    DMESSAGED: str = "dmessaged"
    READY: str = "ready"
    CLOSE: str = "close"
    REACTION: str = "reaction"
    REACTIONR: str = "reactionr"
    TYPING: str = "typing"
    DM_TYPING: str = "dm_typing"

    def __values__(self) -> list:
        return [self.MESSAGEC, self.MESSAGEU, self.MESSAGED, self.DMESSAGEC, self.DMESSAGEU,
                self.DMESSAGED, self.READY, self.CLOSE, self.REACTION, self.REACTIONR,
                self.TYPING, self.DM_TYPING]

    def __type__(self) -> type:
        return str


@final
class Client:
    """
    Class for accessing and sending information in Discord API
    """

    def _raise_unathorized_error(self) -> None:
        raise errors.Unauthorized()

    def __init__(
        self,
        token: str,
        flags: Optional[TypeOf[DisFlags]] = None
    ) -> None:
        """__init__

        Args:
            token (str): Bot token from Discord developers portal
            flags (Optional[TypeOf[DisFlags], optional): Flags of bot. Defaults to None.
        """
        # Type checks
        _type_check(token, str)
        _type_check(flags, optional(TypeOf[DisFlags]))
        # _END

        _u = "https://discord.com/api/v10/users/@me"
        test_j = get(_u, headers={"Authorization": f"Bot {token}"}).json()

        try:
            if test_j["message"] == "401: Unauthorized" and test_j["code"] == 0:
                self._raise_unathorized_error()

        except KeyError:
            ignore()

        del test_j, _u  # Delete variables

        self.token: str = str(token)

        if flags is None:
            self.intflags = DisFlags.default()
        else:
            self.intflags = flags

        self.status = None
        self.debug = False
        self._logger = _BotLogger()
        self._state = ConnectionState(token)
        self._ons = {
            "register": self._on_register,
            "ready": blank,
            "messagec": blank,
            "messageu": blank,
            "messaged": blank,
            "dmessagec": blank,
            "dmessageu": blank,
            "dmessaged": blank,
            "register2": blank,
            "interaction": blank,
            "components": blank,
            "modalsumbit": blank,
            "reaction": blank,
            "reactionr": blank,
            "typing": blank,
            "dm_typing": blank,
            "channel": [blank, 0],
        }
        self._act = None
        self.user = None

        self.api = DisApi(self.token, self.intflags)

        self.isready = False

        self._logger.log("Bot created succesful!")

    @property
    def application(self) -> Application:
        """application
        Bot application object

        Returns:
            Application
        """
        return self._state.application()

    async def _on_register(self, data):
        """
        Register user var
        -----
        :return None:
        """
        self.user: DisUser = self.api.user

        self._state.get(data)

    async def _on_close(self):
        pass

    def event(self) -> Wrapper:
        """event
        Add event to bot

        Returns:
            Wrapper
        """
        def wrapper(func):
            event_type: str = func.__name__

            if event_type.startswith('on_'):
                event_type = event_type.removeprefix('on_')

            if event_type in _all_basic_events:
                if event_type == "close":
                    self._on_close = func
                    self._logger.log("Register on_close() event")
                else:
                    if event_type in [
                        "messagec",
                        "messageu",
                        "messaged",
                        "typing",
                        "dm_typing",
                        "dmessagec",
                        "dmessageu",
                        "dmessaged",
                    ]:
                        if self.intflags >= DisFlags.messages():
                            self._ons[event_type] = func
                            self._logger.log(f"Register on_{event_type}() event")
                        else:
                            self._logger.log("Error: BotEventVisibleError")
                            raise errors.BotEventVisibleError(
                                "messagec(), typing(), dm_typing() and other events"
                                + "don't avaivable right now because flags < DisFlags.messages()"
                            )
                    elif event_type in ["reaction", "reactionr"]:
                        if self.intflags >= DisFlags.reactions():
                            self._ons[event_type] = func
                            self._logger.log(f"Register on_{event_type}() event")
                        else:
                            self._logger.log("Error: BotEventVisibleError")
                            raise errors.BotEventVisibleError(
                                "reaction() and reactionr() events don't"
                                + " avaivable right now because flags < DisFlags.reactions()"
                            )
                    else:
                        self._ons[event_type] = func
                        self._logger.log(f"Register on_{event_type}() event")
            else:
                self._logger.log("Error: BotEventTypeError")
                raise errors.BotEventTypeError("Invalid type of event!")
        return wrapper

    def add_event(
        self, event_type: TypeOf[DisBotEventType], func: Callable
    ) -> None:
        """
        Add event to bot with function and event type
        -----
        :param t: Type of Event
        :param func: Function
        :return None:
        """
        # Type checks
        _type_check(event_type, TypeOf[DisBotEventType])
        _type_check(func, Callable)
        _type_of(event_type, DisBotEventType)
        # _END

        __methodname__ = f"{self.__classname__}.add_event()"

        if isinstance(event_type, DisBotEventType):
            _message = (
                f"Error! In method {__methodname__} was moved"
                "invalid argument! Argument type is DisBotEventType,"
                "but in method have to type is str!"
            )
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
            self._logger.log("Register on_ready() event")
            self._ons["ready"] = func

        return wrapper

    def on_message(self, event_type: Literal["create", "update", "delete"]) -> Wrapper:
        """
        Method for changing on_message() events
        -----
        :param t: Type of on_message() event
        :return Wrapper:
        """
        _ts: List[str] = [
            "create",  # Message create
            "update",  # Message update
            "delete",  # Message delete
        ]

        _mse: List[str] = [
            "messagec",  # Message create
            "messageu",  # Message update
            "messaged",  # Message delete
        ]

        def wrapper(func):
            if event_type in _ts:
                if event_type == _ts[0]:  # Message create
                    self._logger.log("Register on_messagec() event")
                    self._ons[_mse[0]] = func
                elif event_type == _ts[1]:  # Message update
                    self._logger.log("Register on_messageu() event")
                    self._ons[_mse[1]] = func
                elif event_type == _ts[2]:  # Message delete
                    self._logger.log("Register on_messaged() event")
                    self._ons[_mse[2]] = func

        return wrapper

    def on_dm_message(
        self, event_type: Literal["create", "update", "delete"]
    ) -> Wrapper:
        """
        Method for changing on_dm_message() events
        -----
        :param t: Type of on_dm_message() event
        :return Wrapper:
        """
        _ts: List[str] = [
            "create",  # Message create
            "update",  # Message update
            "delete",  # Message delete
        ]

        _mse: List[str] = [
            "dmessagec",  # Message create
            "dmessageu",  # Message update
            "dmessaged",  # Message delete
        ]

        def wrapper(func):
            if event_type in _ts:
                if event_type == _ts[0]:  # Message create
                    self._logger.log("Register on_messagec() event")
                    self._ons[_mse[0]] = func
                elif event_type == _ts[1]:  # Message update
                    self._logger.log("Register on_messageu() event")
                    self._ons[_mse[1]] = func
                elif event_type == _ts[2]:  # Message delete
                    self._logger.log("Register on_messaged() event")
                    self._ons[_mse[2]] = func

        return wrapper

    def on_channel(self, channel_id: int) -> Wrapper:
        """
        On channel event (on_messagec event only in the channel)
        -----
        :param channel_id: Channel id
        :return Wrapper:
        """
        # Type checks
        _type_check(channel_id, int)
        # _END

        def wrapper(func):
            self._logger.log("Register on_channel() event")
            self._ons["channel"] = [func, channel_id]

        return wrapper

    def command(self, name: Optional[str] = MISSING) -> Wrapper:
        """command
        Create command

        Args:
            name (Optional[str], optional): Name of command. Defaults to MISSING.
                                            (if MISSING: func.__name__)

        Returns:
            Wrapper
        """
        # Type checks
        _type_check(name, optional(str))
        # _END

        def wrapper(func, name=name):
            if name is MISSING:
                try:
                    name = func.__name__
                except AttributeError:
                    name = func[1].__name__

            payload = {
                "name": name,
                "type": appc.ApplicationCommandType.TEXT_INPUT,
                "description": "No description",
            }

            try:
                for key in list(func[0].keys()):
                    val = func[0][key]

                    payload[key] = val

                callback = func[1]
            except TypeError:
                callback = func

            self._logger.log("Register command")
            self.api.create_command(payload, callback)

        return wrapper

    def context_menu(self, name: Optional[str] = MISSING):
        """context_menu
        Create context menu

        Args:
            name (Optional[str], optional): Name of context menu. Defaults to MISSING.
                                            (if MISSING: func.__name__)
        """
        # Type checks
        _type_check(name, optional(str))
        # _END

        def wrapper(func, name=name):
            if name is MISSING:
                name = func.__name__

            payload = {"name": name, "type": None}

            # Get type of second argument of function
            sig = signature(func)
            params = dict(sig.parameters)
            param = params[list(params.keys())[1]]
            param_type = param.annotation
            ###

            message_to_log = ""

            if param_type in (Message, DisMessage, DmMessage):
                payload["type"] = appc.ApplicationCommandType.MESSAGE
                message_to_log = "Register message command"

            elif param_type == DisUser:
                payload["type"] = appc.ApplicationCommandType.USER
                message_to_log = "Register user command"

            self._logger.log(message_to_log)
            self.api.create_command(payload, func)

        return wrapper

    def run(
        self,
        status: Literal["online", "dnd", "invisible", "idle"] = "online",
        activity: Optional[Activity] = None,
    ) -> None:
        """
        Running bot
        -----
        :param status: Status for bot user
        :return: None
        """
        # Type checks
        status_type_check = type_check_obj(["online", "dnd", "invisible", "idle"], str)

        _type_check(status, TypeOf[status_type_check])
        _type_of(status, status_type_check)
        _type_check(activity, optional(Activity))
        # _END
        self.isready = True

        self.status = status

        if activity:
            self._act = activity.json()
        else:
            self._act = None

        self._logger.log("Running bot")

        run(self._runner())

    def _raise_internet_error(self):
        _m = "Please turn on your internet!"
        _code = "-1000"
        raise errors.InternetError(_m, _code)

    async def _runner(self) -> None:
        try:
            await self.api.run(self.status, self._ons, debug=self.debug, act=self._act)
        except KeyboardInterrupt:
            self._write_logs()
            await self._on_close()
            await self.api.session.close()
            await self._dissconnenter()
        except requests.exceptions.ConnectionError:
            self._raise_internet_error()

    async def disconnect(self) -> None:
        """
        Disconnect from Gateway
        """
        await self._dissconnenter()

    async def close(self) -> None:
        """
        Disconnect from Gateway
        """
        await self._dissconnenter()

    async def _dissconnenter(self) -> None:
        if self.isready:
            self._logger.log("Disconnect bot")
            await self.api.disconnecter()

    def get_channel(self, channel_id: int) -> Union[DisChannel, DisDmChannel]:
        """
        Get channel from id
        -----
        :param channel_id: Channel Id
        :return Union[DisChannel, DisDmChannel]:
        """
        # Type checks
        _type_check(channel_id, int)
        # _END

        channel = self.api.get_channel_or_thread(channel_id)

        if isinstance(channel, Channel):
            return channel

        _m = "This channel is not channel! Use get_thread() method"
        raise RuntimeError(_m)

    def get_thread(
        self, thread_id: int
    ) -> Union[DisNewsThread, DisThread, DisPrivateThread]:
        """get_thread
        Get thread by id

        Args:
            thread_id (ThreadId): Thread id

        Raises:
            RuntimeError: Argument is not thread id

        Returns:
            Union[DisNewsThread, DisThread, DisPrivateThread]: Getted thread object
        """
        # Type checks
        _type_check(thread_id, int)
        # _END

        thread = self.api.get_channel_or_thread(thread_id)

        if isinstance(thread, Thread):
            return thread

        _m = "This channel is not thread! Use get_channel() method"
        raise RuntimeError(_m)

    def get_guild(self, guild_id: int) -> Guild:
        """
        Get guild from id
        -----
        :param guild_id: Guild Id
        :return Guild:
        """
        # Type checks
        _type_check(guild_id, int)
        # _END

        return self.api.get_guild(guild_id)

    def get_user(self, user_id: int) -> DisUser:
        """
        Get user from id
        -----
        :param user_id: User Id
        :return DisUser:
        """
        # Type checks
        _type_check(user_id, int)
        # _END

        return self.api.get_user(user_id)

    async def change_activity(self, activity: Activity):
        """
        Change activity
        -----
        :param activity: Activity to change
        :return None:
        """
        # Type checks
        _type_check(activity, Activity)
        # _END

        act = activity.json()

        await self.api.fsend_request(
            {
                "op": 3,
                "d": {
                    "since": mktime(datetime.now().timetuple()) * 1000,
                    "afk": self.api.hook.isafk,
                    "status": self.status,
                    "activities": [act],
                },
            }
        )

    def _write_logs(self):
        _datetime = datetime.now()

        tformat = "%d %d %d %d %d %d"

        filename = tformat % (
            _datetime.year,
            _datetime.month,
            _datetime.day,
            _datetime.hour,
            _datetime.minute,
            _datetime.second,
        )

        filename += ".txt"

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r"__logs__")
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        path = Path("__logs__") / filename

        with open(path, "x", encoding="utf-8") as file:
            for i in self._logger.logs:
                file.write(i + "\n")
