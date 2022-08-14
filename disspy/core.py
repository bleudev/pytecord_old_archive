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

# Imports
# Other Packages
import asyncio
from typing import (
    TypeVar,
    Union,
    Coroutine,
    Callable,
    NewType,
    ClassVar,
    Dict,
    List,
    NoReturn,
    Text,
    Any,
    Generic,
    final
)

from enum import Enum, auto
from datetime import datetime
from time import mktime
from aiohttp import ClientSession
from requests import delete, post, get
import colorama


# disspy imports
from disspy.channel import (
    DisChannel,
    DisDmChannel,
    DisMessage,
    DmMessage,
    MessageDeleteEvent,
    DmMessageDeleteEvent
)
from disspy.errors import ClassTypeError
from disspy.guild import DisGuild
from disspy.reaction import DisEmoji, DisReaction, DisRemovedReaction
from disspy.user import DisUser
from disspy.application_commands import Context, _Argument, OptionArgs

JsonOutput = NewType("JsonOutput", Dict[str, Any])

# __all__
__all__: tuple = (
    # Classes for simpler creating other classes
    "JsonOutput",
    "FlowOpcodes",
    "DisFlags",
    "Snowflake",
    "ChannelId",
    "UserId",
    "GuildlId",
    # Private clients
    "Rest",
    "Flow",
    # Main client
    "DisApi"
)

def _mainurl() -> str:
    return "https://discord.com/api/v10/"


class FlowOpcodes:
    """
    Flow Event Opcodes (see Discord Developer Portal docs (topics Gateway)
    """
    DISPATCH: ClassVar[int] = 0
    HEARTBEAT: ClassVar[int] = 1
    IDENTIFY: ClassVar[int] = 2
    PRESENCE_UPDATE: ClassVar[int] = 3
    VOICE_STATE_UPDATE: ClassVar[int] = 4
    RESUME: ClassVar[int] = 6
    RECONNECT: ClassVar[int] = 7
    REQUEST_GUILD_MEMBERS: ClassVar[int] = 8
    INVALID_SESSION: ClassVar[int] = 9
    HELLO: ClassVar[int] = 10
    HEARTBEAT_ACK: ClassVar[int] = 11

    @staticmethod
    def rotated_dict() -> Dict[int, str]:
        """
        Return rotated dict with opcode and this name
        -----
        :return Dict[int, str]: Rotated dict
        """
        return {
            0:  "DISPATCH",
            1:  "HEARTBEAT",
            2:  "IDENTIFY",
            3:  "PRESENCE UPDATE",
            4:  "VOICE STATE UPDATE",
            6:  "RESUME",
            7:  "RECONNECT",
            8:  "REQUEST GUILD MEMBERS",
            9:  "INVALID SESSION",
            10: "HELLO",
            11: "HEARTBEAT ACK"
        }


colorama.init()  # Init Colorama


class _DebugLoggingWebsocket:
    """
    Debug tool for Websocket
    """
    def __new__(cls, *args, **kwargs) -> Text:
        _data: dict = args[0]

        try:
            _send = kwargs["send"]
        except KeyError:
            _send = False

        try:
            _isevent = kwargs["isevent"]
        except KeyError:
            _isevent = False

        try:
            _op = kwargs["op"]
        except KeyError:
            _op = 0

        _datetime = datetime.now()

        _second = _datetime.second if _datetime.second > 9 else f"{_datetime.second}0"

        _date = f"{_datetime.day}/{_datetime.month}/{_datetime.year}"
        _time = f"{_datetime.hour}:{_datetime.minute}:{_second}.{str(_datetime.microsecond)[:2]}"

        _result = f"{colorama.Fore.CYAN}[{_date}: {_time}]{colorama.Fore.RESET} "

        _op_str = FlowOpcodes.rotated_dict()[_op]
        _op_str = _op_str.capitalize()

        _2part = f" | {_op_str}:{colorama.Fore.RESET} {_data}"

        try:
            del _data["d"]["_trace"]
        except KeyError:
            pass
        except TypeError:
            pass

        if _send:
            if _op == 2:
                _data["d"]["token"] = "TOKEN"

            if _op == 11:
                _op_str = "Heartbeat ACK"

            _result += f"{colorama.Fore.GREEN}Sending Request{colorama.Fore.RED}"
        else:
            if _isevent:
                if _op == 11:
                    _op_str = "Heartbeat ACK"

                _result += f"{colorama.Fore.YELLOW}Getting Event{colorama.Fore.RED}"
            else:
                if _op == 11:
                    _op_str = "Heartbeat ACK"

                _result += f"{colorama.Fore.YELLOW}Getting Responce{colorama.Fore.RED}"

        _result += _2part

        return _result


class _DebugLoggingAwaiting:
    def __new__(cls, gateway_event_name, event_name):
        _datetime = datetime.now()

        _second = _datetime.second if _datetime.second > 9 else f"{_datetime.second}0"

        _date = f"{_datetime.day}/{_datetime.month}/{_datetime.year}"
        _time = f"{_datetime.hour}:{_datetime.minute}:{_second}.{str(_datetime.microsecond)[:2]}"

        _result = f"{colorama.Fore.CYAN}[{_date}: {_time}]{colorama.Fore.RESET} "

        _result += f'{colorama.Fore.RED}Awaiting event "{gateway_event_name}": '
        _result += f'{colorama.Fore.YELLOW}{event_name}(){colorama.Fore.RESET}'

        return _result


class _RequestsUserClass:
    """
    Class for Getting and Posting data in Discord
    """
    @staticmethod
    async def _aiopost(url, data, headers) -> JsonOutput:
        """
        Aiohttp post
        -----
        :param url: Url for post
        :param data: Json data for post
        :param headers: Headers for post
        :return JsonOutput:
        """
        async with ClientSession(headers=headers) as _s:
            async with _s.post(url=url, data=data) as _p:
                return _p.json()

    @staticmethod
    def _post(url: str, data: dict, headers: dict) -> JsonOutput:
        """
        Request post
        -----
        :param url: Url for post
        :param data: Json data for post
        :param headers: Headers for post
        :return JsonOutput:
        """
        return post(url=url, json=data, headers=headers).json()

    @staticmethod
    def _get(url: str, headers: dict) -> JsonOutput:
        """
        Request get
        -----
        :param url: Url for get
        :param headers: Headers for get
        :return JsonOutput:
        """
        return get(url=url, headers=headers).json()


class _FlowEvent:
    """
    Event object with type, session id, data and opcode

    :var type (str): Type of event (For example, "READY")
    :var session (str): Session id of Flow
    :var data (dict): Event's JSON data
    :var opcode (int): Event's OpCode (For example, 0 (Dispatch))
    """

    def __init__(self, json) -> NoReturn:
        """
        Init object

        :param json: JSON data
        """
        try:
            self.type = json["t"]
            self.session = json["s"]
            self.data = json["d"]
            self.opcode = json["op"]
            self.json = json
        except TypeError:
            self.type = "ERROR"
            self.session = None
            self.data = {
                "type": "json data is not dict!"
            }
            self.opcode = 0
            self.json = {
                "t": "ERROR",
                "s": None,
                "d": {},
                "op": 0
            }


class _AutoFlags(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return 1 << count

class _Intents(_AutoFlags):
    GUILDS = auto()
    GUILD_MEMBERS = auto()
    GUILD_BANS = auto()
    GUILD_EMOJIS_AND_STICKERS = auto()
    GUILD_INTEGRATIONS = auto()
    GUILD_WEBHOOKS = auto()
    GUILD_INVITES = auto()
    GUILD_VOICE_STATES = auto()
    GUILD_PRESENCES = auto()
    GUILD_MESSAGES = auto()
    GUILD_MESSAGE_REACTIONS = auto()
    GUILD_MESSAGE_TYPING = auto()
    DIRECT_MESSAGES = auto()
    DIRECT_MESSAGE_REACTIONS = auto()
    DIRECT_MESSAGE_TYPING  = auto()
    MESSAGE_CONTENT = auto()
    GUILD_SCHEDULED_EVENTS = auto()


class DisFlags:
    """
    The class for using intents in bots

    :methods:
        :method: default()
            Implements GUILD_MESSAGES and default intents
        :method: all()
            Implements all Gateway Intents
    """
    __classname__: str = "DisFlags"

    def __all__(self) -> List[str]:
        return [str(self.default()), str(self.all())]

    @staticmethod
    def default() -> int:
        """
        Implements:
            None

        :return int: integer value of intents
        """
        return int(_Intents.GUILD_INTEGRATIONS.value)

    @staticmethod
    def messages() -> int:
        """
        Implements:
            1. GUILD_MESSAGES
            2. GUILD_MESSAGE_TYPING
            3. DIRECT_MESSAGES
            4. DIRECT_MESSAGE_TYPING
            5. MESSAGE_CONTENT (Privilleged intent)

        :return int: integer value of intents
        """

        _typings = _Intents.GUILD_MESSAGE_TYPING.value + _Intents.DIRECT_MESSAGE_TYPING.value
        _messages = _Intents.GUILD_MESSAGES.value + _Intents.DIRECT_MESSAGES.value
        _content = _Intents.MESSAGE_CONTENT.value

        return int(_Intents.GUILD_INTEGRATIONS.value + _typings + _messages + _content)

    @staticmethod
    def reactions() -> int:
        """
        Implements:
            1. GUILD_MESSAGE_REACTIONS
            2. DIRECT_MESSAGE_REACTIONS

        :return int: integer value of intents
        """
        _dm_reactions = _Intents.DIRECT_MESSAGE_REACTIONS.value
        _reactions = _Intents.GUILD_MESSAGE_REACTIONS.value + _dm_reactions

        return int(_Intents.GUILD_INTEGRATIONS.value + _reactions)

    @staticmethod
    def all() -> int:
        """
        Implements:
            1.  GUILDS
            2.  GUILD_MEMBERS (Privileged intent)
            3.  GUILD_BANS
            4.  GUILD_EMOJIS_AND_STICKERS
            5.  GUILD_INTEGRATIONS
            6.  GUILD_WEBHOOKS
            7.  GUILD_INVITES
            8.  GUILD_VOICE_STATES
            9.  GUILD_PRESENCES (Privileged intent)
            10. GUILD_MESSAGES
            11. GUILD_MESSAGE_REACTIONS
            12. GUILD_MESSAGE_TYPING
            13. DIRECT_MESSAGES
            14. DIRECT_MESSAGE_REACTIONS
            15. DIRECT_MESSAGE_TYPING
            16. GUILD_SCHEDULED_EVENTS
            17. MESSAGE_CONTENT (Privileged intent)

        :return int: integer value of intents
        """
        result = 0

        for i in _Intents:
            result += i.value

        return int(result)


T = TypeVar("T", str, int)


@final
class Snowflake(Generic[T]):
    """
    Class info

    Snowflake is using for simpled work with tokens and ids.

    :var self.isid:
    """

    def __init__(self, value: T) -> NoReturn:
        if isinstance(value, int):
            self.isid = True
            self.istoken = False
            self.value: int = value
        elif value.isdigit():
            self.isid = True
            self.istoken = False
            self.value = int(value)
        else:
            self.isid = False
            self.istoken = True
            self.value = value

    def __int__(self) -> int:
        if not self.isid:
            raise ClassTypeError("Class Value is str, but this method needs for int!")

        return int(self.value)

    def __str__(self) -> str:
        if not self.istoken:
            raise ClassTypeError("Class Value is int, but this method needs for str!")

        return str(self.value)


ChannelId = NewType("ChannelId", int)
UserId = NewType("UserId", int)
GuildlId = NewType("GuildId", int)


@final
class Rest:
    """
    Rest class
    """
    __classname__: str = "Rest"

    def __init__(self, token: str):
        self._headers = {'Authorization': f'Bot {token}', "content-type": "application/json"}

        self.__slots__ = [self._headers]

    def get(self, goal: str, goal_id: Union[int, Snowflake]) -> Union[JsonOutput, None]:
        """
        :param goal: guild/channel/user
        :param id: id of guild/channel/user
        :return JsonOutput: Json answer from Discord API server
        """
        goal_id = int(goal_id)

        if goal.casefold() == 'guild':
            _url = f'{_mainurl()}guilds/{str(goal_id)}'
            return get(url=_url,
                       headers=self._headers).json()

        if goal.casefold() == 'channel':
            _url = f'{_mainurl()}channels/{str(goal_id)}'

            return get(url=_url,
                       headers=self._headers).json()

        if goal.casefold() == "user":
            _url = f'{_mainurl()}users/{str(goal_id)}'

            return get(url=_url,
                       headers=self._headers).json()

        return None

    def fetch(self, channel_id, message_id) -> JsonOutput:
        """fetch()

        Args:
            channel_id (_type_): Channel id
            message_id (_type_): Message id from this channel

        Returns:
            JsonOutput: Json data about fetched message
        """
        _channel_id, _message_id = [str(channel_id), str(message_id)]

        _url = f"{_mainurl()}channels/{_channel_id}/messages/{_message_id}"

        return get(_url, self._headers).json()

    async def send_message(self, channel_id, json_post):
        """send_message
        Send messages in channels

        Args:
            channel_id (int): Channel id
            json_post (dict): Json data for send

        Returns:
            dict: Json output
        """
        _url = f"{_mainurl()}channels/{channel_id}/messages"

        async with ClientSession(headers=self._headers) as session:
            async with session.post(_url, data=json_post) as post_process:
                j = await post_process.json()
                return j


@final
class Flow:
    """
    Flow class was created for opening and working with Discord Gateway
    """
    __classname__: str = "Flow"

    def __init__(self, gateway_version: int, token: str, intents: int):

        self.on_channel__id = 0
        self.user_id = "null"
        self.heartbeat_interval = 0

        self.gateway_version: int = gateway_version

        self.intents = intents
        self.activity = None
        self.status = "online"

        # ISes
        self.isrunning = False
        self.isafk = False

        self.token = token
        self._rest = Rest(token)
        self._debug = False

        self._headers = {}

        self.websocket = None
        self.ons = None

    # Event methods
    async def on_channel(self, message: DisMessage):
        """on_channel
        "MESSAGE CREATE" event, but only in one channel

        Args:
            message (DisMessage): Message that was created
        """
        return message.content  # For PyLint

    async def register(self, data):
        """register
        Register user id

        Args:
            data (dict): Data of "READY" event
        """
        self.user_id = data["user"]["id"]

    # Sending/Getting
    async def send_request(self, data, websocket):
        """send_request
        Send json request to Gateway

        Args:
            data (dict): Json data
            ws (Any): Aiohttp websocket

        Returns:
            dict: Your json data
        """
        await websocket.send_json(data)

        if self._debug:
            print(_DebugLoggingWebsocket(data, send=True, isevent=False, op=data["op"]))

        return data

    async def get_responce(self, websocket):
        """get_responce
        Get json output from Gateway

        Args:
            ws (Any): Aiohttp websocket

        Returns:
            dict: Json output
        """
        try:
            j = await websocket.receive_json()
        except TypeError:
            return

        if self._debug:
            try:
                if j["t"]:
                    print(_DebugLoggingWebsocket(j, send=False, isevent=True, op=j["op"]))
                else:
                    print(_DebugLoggingWebsocket(j, send=False, isevent=False, op=j["op"]))
            except KeyError:
                print(_DebugLoggingWebsocket(j, send=False, isevent=False, op=j["op"]))

        return j

    # Runners
    async def run(self, ons, status, debug, act):
        """run
        Run Flow (Gateway)

        Args:
            ons (dict): Dict with _type_: _func_ model for awaiting this events
            status (str): Status of bot
            debug (bool): Debug id enabled?
            act (dict): Activity of bot
        """
        self._debug = debug
        self.status = status
        self.activity = act
        self.ons = ons

        # Registering events
        if ons["channel"][0] is not None:
            self.on_channel = ons["channel"][0]
            self.on_channel__id = ons["channel"][1]

        # Other
        self.isrunning = True
        self.isafk = False

        await self._runner()

    async def _runner(self):
        async with ClientSession() as session:
            async with session.ws_connect(
                f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json") as websocket:
                self.websocket = websocket

                j = await self.get_responce(websocket)

                interval = j["d"]["heartbeat_interval"]


                await self.send_request({"op": 2, "d": {
                    "token": self.token,
                    "intents": self.intents,
                    "properties": {
                        "$os": "linux",
                        "$browser": "disspy",
                        "$device": "disspy"
                    },
                    "presence": {
                        "since": mktime(datetime.now().timetuple()) * 1000,
                        "afk": self.isafk,
                        "status": self.status,
                        "activities": [self.activity]
                    }
                }}, websocket)

                self.isrunning = True

                await asyncio.wait(
                    fs=[self.heartbeat(websocket, interval / 1000),
                        self._events_checker(websocket)])  # Run Gateway client

    async def heartbeat(self, websocket, interval):
        """heartbeat
        Function with sending heartbeating to Gateway

        Args:
            websocket (Any): Aiohttp websocket
            interval (int): Heartbeat interval
        """
        while True:
            await self.send_request({"op": 1, "d": None, "t": None}, websocket)

            await asyncio.sleep(interval)

    async def _events_checker(self, websocket):
        while True:
            event_json = await self.get_responce(websocket)
            event = _FlowEvent(event_json)

            try:
                if event.type == "READY":
                    await self.register(event.data)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "register"))

                    await self.ons["register2"](event.data)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_register2"))

                    await self.ons["register"]()

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_register"))

                    await self.ons["ready"]()

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_ready"))

                elif event.type == "MESSAGE_CREATE":
                    _u: str = f"https://discord.com/api/v10/channels/{event.data['channel_id']}"

                    if not event.data["author"]["id"] == self.user_id:
                        async with ClientSession(
                            headers={'Authorization': f'Bot {self.token}',
                                     'content-type': 'application/json'}) as session:
                            async with session.get(_u) as data:
                                j = await data.json()

                                if j["type"] == 0:
                                    _m = DisMessage(event.data, self.token)

                                    if int(event.data["channel_id"]) == int(self.on_channel__id):
                                        await self.on_channel(_m)

                                        if self._debug:
                                            print(_DebugLoggingAwaiting(event.type, "on_channel"))


                                    await self.ons["messagec"](_m)

                                    if self._debug:
                                        print(_DebugLoggingAwaiting(event.type, "on_messagec"))
                                elif j["type"] == 1:
                                    _m = DmMessage(event.data, self.token)

                                    await self.ons["dmessagec"](_m)

                                    if self._debug:
                                        print(_DebugLoggingAwaiting(event.type, "on_dmessagec"))

                elif event.type == "MESSAGE_UPDATE":
                    _u: str = f"https://discord.com/api/v10/channels/{event.data['channel_id']}"

                    if not event.data["author"]["id"] == self.user_id:
                        async with ClientSession(
                            headers={'Authorization': f'Bot {self.token}',
                                     'content-type': 'application/json'}) as session:
                            async with session.get(_u) as data:
                                j = await data.json()

                                if j["type"] == 0:
                                    _m = DisMessage(event.data, self.token)

                                    await self.ons["messageu"](_m)

                                    if self._debug:
                                        print(_DebugLoggingAwaiting(event.type, "on_messageu"))
                                elif j["type"] == 1:
                                    _m = DmMessage(event.data, self.token)

                                    await self.ons["dmessageu"](_m)

                                    if self._debug:
                                        print(_DebugLoggingAwaiting(event.type, "on_dmessageu"))

                elif event.type == "MESSAGE_DELETE":
                    _u = f"https://discord.com/api/v10/channels/{event.data['channel_id']}"

                    async with ClientSession(
                        headers={'Authorization': f'Bot {self.token}',
                                 'content-type': 'application/json'}) as session:
                        async with session.get(_u) as data:
                            j = await data.json()

                            if j["type"] == 0:
                                _e = MessageDeleteEvent(event.data, self.token)

                                await self.ons["messaged"](_e)

                                if self._debug:
                                    print(_DebugLoggingAwaiting(event.type, "on_messaged"))
                            elif j["type"] == 1:
                                _e = DmMessageDeleteEvent(event.data, self.token)

                                await self.ons["dmessaged"](_e)

                                if self._debug:
                                    print(_DebugLoggingAwaiting(event.type, "on_dmessaged"))

                elif event.type == "INTERACTION_CREATE":
                    if event.data["type"] == 2:  # Application Commands
                        await self.ons["interaction"](
                            event.data["token"], event.data["id"], event.data["data"]["name"],
                            self.token, event.data["type"], event.data, event.data["data"]["type"])

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_interaction"))
                    if event.data["type"] == 3 or event.data["type"] == 4:  # Components
                        await self.ons["components"](event.data)

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_components"))

                    if event.data["type"] == 5:  # Modal Sumbit
                        await self.ons["modalsumbit"](event.data)

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_modalsumbit"))

                elif event.type == "MESSAGE_REACTION_ADD":
                    _u = DisUser(event.data["member"]["user"], self.token)
                    _m_id = int(event.data["message_id"])
                    _c_id = int(event.data["channel_id"])
                    _g_id = int(event.data["guild_id"])

                    _e_json = event.data["emoji"]

                    if _e_json["id"] is None:
                        _e = DisEmoji(unicode=_e_json["name"])
                    else:
                        _e = DisEmoji(name=_e_json["name"], emoji_id=int(_e_json["id"]))

                    _r = DisReaction(_u, _m_id, _c_id, _g_id, _e, self.token)

                    await self.ons["reaction"](_r)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_reaction"))

                elif event.type == "MESSAGE_REACTION_REMOVE":
                    _m_id = int(event.data["message_id"])
                    _c_id = int(event.data["channel_id"])
                    _g_id = int(event.data["guild_id"])

                    _e_json = event.data["emoji"]

                    if _e_json["id"] is None:
                        _e = DisEmoji(unicode=_e_json["name"])
                    else:
                        _e = DisEmoji(name=_e_json["name"], emoji_id=int(_e_json["id"]))

                    _r = DisRemovedReaction(_m_id, _c_id, _g_id, _e, self.token)

                    await self.ons["reactionr"](_r)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_reactionr"))

                elif event.type == "TYPING_START":
                    try:
                        if event.data["guild_id"]:
                            _u: DisUser = DisUser(event.data["member"]["user"], self.token)
                            _c: DisChannel = DisChannel(event.data["channel_id"], self.token)

                            await self.ons["typing"](_u, _c)

                            if self._debug:
                                print(_DebugLoggingAwaiting(event.type, "on_typing"))
                        else:
                            _u_id = event.data["user_id"]
                            _u_json = Rest(self.token).get("user", _u_id)

                            _u: DisUser = DisUser(_u_json, self.token)
                            _c: DisDmChannel = DisDmChannel(event.data["channel_id"], self.token)

                            await self.ons["dm_typing"](_u, _c)

                            if self._debug:
                                print(_DebugLoggingAwaiting(event.type, "on_dm_typing"))
                    except KeyError:
                        _u_id = event.data["user_id"]
                        _u_json = Rest(self.token).get("user", _u_id)

                        _u: DisUser = DisUser(_u_json, self.token)
                        _c: DisDmChannel = DisDmChannel(event.data["channel_id"], self.token)

                        await self.ons["dm_typing"](_u, _c)

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_dm_typing"))
            except TypeError:
                pass

            await asyncio.sleep(0.5)

    async def disconnecter(self):
        """disconnecter
        Disconnect from Gateway
        """
        await self.websocket.close()


@final
class DisApi(_RequestsUserClass):
    """DisApi
    Class for init Rest and Flow event and edit they
    """
    def __init__(self, token: str, intents):
        """
        Init Class

        :param token: Token of bot (from Discord Developer Portal)
        :param intents: Intents of bot
        :param application_id: Application id of bot (from Discord Developer Portal)
        """
        super().__init__()

        self.comsevs = {}
        self._headers = {'Authorization': f'Bot {token}', "content-type": "application/json"}
        self.app_commands_jsons = []

        self._on_ready = None
        self._on_messagec = None
        self.token = token

        self.flow = Flow(10, self.token, intents)
        self._r = Rest(self.token)

        self.app_commands = []
        self.raw_app_commands = []

        self.user = None
        self._debug = False

        self.app_commands.append({})  # Slash Commands
        self.app_commands.append({})  # User Commands
        self.app_commands.append({})  # Message Commands

    def fetch(self, channel_id, message_id) -> DisMessage:
        """fetch
        Fetch message by its id and channel id

        Args:
            channel_id (int): Channel id
            message_id (int): Message id

        Returns:
            DisMessage: Fetched message
        """
        _url = f"{_mainurl()}channels/{channel_id}/messages/{message_id}"

        _d = self._r.fetch(channel_id, message_id)

        return DisMessage(_d, self.token)

    async def run(self, status, ons: Dict[Text, Callable], debug: bool,
                  act: Dict[str, Any]) -> NoReturn:
        """
        Run the flow of DisApi or run the bot.
        Running bot in Discord, changing status and registering
        and running events in discord Gateway
        -----
        :param status: Status of bot in Discord (default is "online")
        :param ons: Events in dict format (Dict[Text, Awaitable])
        :param debug: Process is debug?
        :param act: Bot activity
        :return None:
        """
        ons["register2"] = self._register2
        ons["interaction"] = self._on_interaction
        ons["components"] = self._on_components
        ons["modalsumbit"] = self._on_modal_sumbit

        self._debug = debug

        await self.flow.run(ons, status, debug, act)

    async def _register2(self, data: dict):
        # pass
        self.user: DisUser = self.get_user(self.flow.user_id)

        if self._debug:
            print(f"{colorama.Fore.YELLOW}Registering application commands...{colorama.Fore.RESET}")

        app_id = data["application"]["id"]

        _url = f"{_mainurl()}applications/{app_id}/commands"

        application_commands_from_server = get(_url, headers=self._headers).json()
        application_commands_from_code = self.app_commands_jsons

        if not application_commands_from_server and not application_commands_from_code:
            pass

        elif not application_commands_from_server and application_commands_from_code:
            for code in application_commands_from_code:
                post_event = post(_url, json=code, headers=self._headers).json()

                if self._debug:
                    print(f"{colorama.Fore.BLUE}POST |{colorama.Fore.RESET} {post_event}")

        elif not application_commands_from_code and application_commands_from_server:
            for server in application_commands_from_server:
                delete(f"{_url}/{server['id']}", headers=self._headers)

                if self._debug:
                    print(f"{colorama.Fore.CYAN}DELETE |{colorama.Fore.RESET} {server}")
        elif application_commands_from_code and application_commands_from_server:
            for server in application_commands_from_server:
                delete(f"{_url}/{server['id']}", headers=self._headers)

                if self._debug:
                    print(f"{colorama.Fore.CYAN}DELETE |{colorama.Fore.RESET} {server}")

            for code in application_commands_from_code:
                post_event = post(_url, json=code, headers=self._headers).json()

                if self._debug:
                    print(f"{colorama.Fore.BLUE}POST |{colorama.Fore.RESET} {post_event}")

        if self._debug:
            server_app_commands = get(_url, headers=self._headers).json()

            print(f"{colorama.Fore.YELLOW}Current commands on server: {colorama.Fore.RESET}", end="")
            print(server_app_commands)
            print(f"{colorama.Fore.GREEN}Regsiter is completed!")

    async def _on_interaction(self, token, interaction_id, command_name, bot_token: str,
                              interaction_type, data: JsonOutput, type_of_command=None) -> NoReturn:
        if interaction_type == 2:
            _ctx = Context(token, interaction_id, bot_token)

            try:
                if type_of_command == 3:  # Message Commands
                    resolved: dict = data["data"]["resolved"]["messages"]

                    _m_id = list(resolved.keys())[0]
                    _m_d: dict = resolved[_m_id]

                    try:
                        _m_d["id"] = _m_id
                    except KeyError:
                        _m_d.setdefault("id", _m_id)

                    _m = DisMessage(_m_d, self.token)

                    await self.app_commands[type_of_command - 1][command_name](_ctx, _m)

                elif type_of_command == 2:  # User Commands
                    resolved: dict = data["data"]["resolved"]["users"]

                    _u_id = list(resolved.keys())[0]
                    _u_d: dict = resolved[_u_id]

                    try:
                        _u_d["id"] = _u_id
                    except KeyError:
                        _u_d.setdefault("id", _u_id)

                    _u = DisUser(_u_d, self.token)

                    await self.app_commands[type_of_command - 1][command_name](_ctx, _u)

                elif type_of_command == 1:  # Slash Commands
                    _args = []

                    try:
                        for option in data["data"]["options"]:
                            _args.append(_Argument(option["name"],
                                                    option["type"],
                                                    option["value"]))
                    except KeyError:
                        _args = []

                    func = self.app_commands[type_of_command - 1][command_name]

                    await func(_ctx, OptionArgs(_args))
                else:
                    pass
            except KeyError:
                pass

    async def _on_components(self, data):
        if data["data"]["component_type"] == 2:
            _ctx = Context(data["token"], data["id"], self.token)
            await self.comsevs[data["data"]["custom_id"]](_ctx)

        if data["data"]["component_type"] == 3:
            _ctx = Context(data["token"], data["id"], self.token)
            _vs = data["data"]["values"]
            await self.comsevs[data["data"]["custom_id"]](_ctx, _vs)

    async def _on_modal_sumbit(self, data):
        _ctx = Context(data["token"], data["id"], self.token)
        coms = data["data"]["components"][0]["components"]
        _v = ""

        for i in coms:
            if i["custom_id"] == data["data"]["custom_id"]:
                _v = i["value"]

        await self.comsevs[data["data"]["custom_id"]](_ctx, _v)

    def get_user(self, user_id: UserId) -> DisUser:
        """
        Get user by id
        -----
        :param user_id: id of user
        :return DisUser: User
        """

        return DisUser(self.get_user_json(user_id), self.token)

    def get_user_json(self, user_id: UserId) -> JsonOutput:
        """
        Get user by id (Json Output)
        -----
        :param user_id: id of user
        :return JsonOutput:
        """
        user_id = int(user_id)  # If Snowflake this will be int

        return self._r.get("user", user_id)

    def get_channel(self, channel_id: ChannelId) -> DisChannel:
        """
        Get channel by id
        -----
        :param channel_id: id of channel
        :return DisChannel:
        """
        channel_id = int(channel_id)  # If Snowflake this will be int

        return DisChannel(channel_id, self)

    def get_channel_json(self, channel_id: ChannelId) -> JsonOutput:
        """
        Get channel by id (Json Output)
        -----
        :param channel_id: id of channel
        :return JsonOutput:
        """
        channel_id = int(channel_id)  # If Snowflake this will be int

        return self._r.get("channel", channel_id)

    def get_guild(self, guild_id: GuildlId) -> DisGuild:
        """
        Get guild by id

        :param guild_id: id of guild
        :return DisGuild:
        """
        guild_id = int(guild_id)  # If Snowflake this will be int

        return DisGuild(guild_id, self)

    def get_guild_json(self, guild_id: GuildlId) -> JsonOutput:
        """
        Get guild by id (Json Output)

        :param guild_id: id of guild
        :return JsonOutput:
        """

        guild_id = int(guild_id)  # If Snowflake this will be int

        return self._r.get("guild", guild_id)

    def create_command(self, payload: dict, func: Callable[..., Coroutine[Any, Any, Any]]):
        """create_command
        Create application command

        Args:
            payload (dict): Json data of command
            func (Awaitable): Function for awaiting command
        """
        def app_func_register(number):
            self.app_commands[number][payload["name"]] = func

        if payload["type"] == 1:
            # Register interaction func to Slash Commands
            self.app_commands_jsons.append(payload)

            app_func_register(0)

        elif payload["type"] == 2:
            # Register interaction func to User Commands
            try:
                if not payload["description"]:
                    self.app_commands_jsons.append(payload)

                    app_func_register(1)
            except KeyError:
                self.app_commands_jsons.append(payload)

                app_func_register(1)

        elif payload["type"] == 3:
            # Register interaction func to Message Commands
            try:
                if not payload["description"]:
                    self.app_commands_jsons.append(payload)

                    app_func_register(2)
            except KeyError:
                self.app_commands_jsons.append(payload)

                app_func_register(2)

    async def fsend_request(self, data: dict):
        """fsend_request()

        Send to Flow websocket a json request

        Args:
            data (dict): Json data for sending request
        """
        await self.flow.send_request(data, self.flow.websocket)
