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
from aiohttp import ClientSession
from requests import get, post, Response
import colorama

# Typing imports
from typing import (
    Type,
    TypeVar,
    Union,
    Optional,
    Awaitable,
    Callable,
    NewType,
    ClassVar,
    Dict,
    List,
    NoReturn,
    Text,
    Any,
    Generic,
    final,
    overload
)

# disspy imports
from disspy.application_commands import Context
from disspy.channel import DisChannel, DisDm
from disspy.errors import ClassTypeError
from disspy.guild import DisGuild
from disspy.message import DisMessage
from disspy.user import DisUser
from disspy.embed import DisEmbed

__name__: str = "core"

__package__: str = "disspy"

__all__: tuple[str] = (
    # Classes for simpler creating other classes
    "FlowOpcodes",
    "DisFlags",
    "Showflake",
    # Private clients
    "Rest",
    "Flow",
    # Main client
    "DisApi"
)


JsonOutput = NewType("JsonOutput", Dict[str, Any])


def _mainurl() -> str:
    return "https://discord.com/api/v9/"


class FlowOpcodes:
    """
    Flow Event Opcodes (see Discord Developer Portal docs (topics Gateway)
    """
    _T = TypeVar("FlowOpcodes")

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

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of class
        -----
        :return TypeVar: Type of class
        """
        return self._T


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

        _result = ""

        _op_str = FlowOpcodes.rotated_dict()[_op]
        _op_str = _op_str.capitalize()

        try:
            del _data["d"]["_trace"]
        except KeyError:
            pass
        except TypeError:
            pass

        if _send:
            if _op == 2:
                _data["d"]["token"] = "TOKEN"

            _result = f"{colorama.Fore.GREEN}Sending Request{colorama.Fore.RED} | {_op_str}:{colorama.Fore.RESET} {_data}"
        else:
            if _isevent:
                _result = f"{colorama.Fore.YELLOW}Getting Event{colorama.Fore.RED} | {_op_str}:{colorama.Fore.RESET} {_data}"
            else:
                if _op == 11:
                    _op_str = "Heartbeat ACK"

                _result = f"{colorama.Fore.YELLOW}Getting Responce{colorama.Fore.RED} | {_op_str}:{colorama.Fore.RESET} {_data}"

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

    _T: TypeVar = TypeVar(__classname__)

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of class
        -----
        :return TypeVar: Type of class
        """
        return self._T

    def __all__(self) -> List[str]:
        return [str(self.default()), str(self.all())]

    @staticmethod
    def default() -> int:
        """
        Implements:
            None

        :return int: integer value of intents
        """
        return 0

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
        return 55808

    @staticmethod
    def reactions() -> int:
        """
        Implements:
            1. GUILD_MESSAGE_REACTIONS
            2. DIRECT_MESSAGE_REACTIONS

        :return int: integer value of intents
        """
        return 9216

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
            17. MESSAGE_CONTENT (Privilleged intent)

        :return int: integer value of intents
        """
        return 98303


T = TypeVar("T", str, int)


@final
class Showflake(Generic[T]):
    """
    Class info

    Showflake is using for simpled work with tokens and ids.

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
        else:
            return int(self.value)

    def __str__(self) -> str:
        if not self.istoken:
            raise ClassTypeError("Class Value is int, but this method needs for str!")
        else:
            return str(self.value)


ChannelId = NewType("ChannelId", Union[int, Showflake])
UserId = NewType("UserId", Union[int, Showflake])
GuildlId = NewType("GuildId", Union[int, Showflake])


@final
class Rest(_RequestsUserClass):
    __classname__: str = "Rest"

    _T: TypeVar = TypeVar(__classname__)

    def __init__(self, token: str):
        super().__init__()

        self._headers = {'Authorization': f'Bot {token}', "content-type": "application/json"}

        self.__slots__ = [self._headers]

    @property
    def __class__(self: _T) -> Type[_T]:
        return Type[self._T]

    def get(self, goal: str, id: Union[int, Showflake]) -> JsonOutput:
        """
        :param goal: guild/channel/user
        :param id: id of guild/channel/user
        :return JsonOutput: Json answer from Discord API server
        """
        id = int(id)

        if goal.casefold() == 'guild':
            _url = f'{_mainurl()}guilds/{str(id)}'
            return get(url=_url,
                       headers=self._headers).json()

        elif goal.casefold() == 'channel':
            _url = f'{_mainurl()}channels/{str(id)}'

            return get(url=_url,
                       headers=self._headers).json()

        elif goal.casefold() == "user":
            _url = f'{_mainurl()}users/{str(id)}'

            return get(url=_url,
                       headers=self._headers).json()

    def fetch(self, channel_id, message_id) -> JsonOutput:
        _channel_id, _message_id = [str(channel_id), str(message_id)]

        _url = f"{_mainurl()}channels/{_channel_id}/messages/{_message_id}"

        return get(_url, self._headers).json()

    async def send_message(self, channel_id, json_post):
        _url = f"{_mainurl()}channels/{channel_id}/messages"

        async with ClientSession(headers=self._headers) as s:
            async with s.post(_url, data=json_post) as p:
                j = await p.json()
                return j


@final
class Flow:
    __classname__: str = "Flow"

    _T = TypeVar(__classname__)

    @property
    def __class__(self: _T) -> Type[_T]:
        return self._T

    def __init__(self, gateway_version: int, token: str, intents: int,
                 activity: dict):

        self.user_id = "null"
        self.heartbeat_interval = 0

        self.gateway_version: int = gateway_version

        self.intents = intents
        self.activity = activity
        self.status = "online"

        # ISes
        self.isrunning = False
        self.isafk = False

        self.token = token
        self._rest = Rest(token)
        self._debug = False

        self._headers = {}

        self.ws = None

    # Event methods
    async def on_ready(self):
        pass

    async def on_messagec(self, m):
        pass

    async def on_interaction(self, token, id, command_name: Text, bot_token: Showflake[str], type: int, data: JsonOutput, type_of_command: Optional[int] = None):
        pass

    async def on_register(self):
        pass

    async def register2(self):
        pass

    async def on_reaction(self, r):
        pass

    async def on_reactionr(self, r):
        pass

    async def on_typing_start(self, u: DisUser, channel: DisChannel):
        pass

    async def on_dm_typing_start(self, u: DisUser, channel: DisDm):
        pass

    async def register(self, d):
        self.user_id = d["user"]["id"]

    # Sending/Getting
    async def send_request(self, data, ws):
        await ws.send_json(data)

        if self._debug:
            print(_DebugLoggingWebsocket(data, send=True, isevent=False, op=data["op"]))

        return data

    async def get_responce(self, ws):
        try:
            j = await ws.receive_json()
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
        self._debug = debug
        self.status = status
        self.activity = act

        # Registering events
        if ons["ready"] is not None:
            self.on_ready = ons["ready"]
        if ons["messagec"] is not None:
            self.on_messagec = ons["messagec"]
        if ons["reaction"] is not None:
            self.on_reaction = ons["reaction"]
        if ons["reactionr"] is not None:
            self.on_reactionr = ons["reactionr"]
        if ons["typing"] is not None:
            self.on_typing_start = ons["typing"]
        if ons["dm_typing"] is not None:
            self.on_dm_typing_start = ons["dm_typing"]

        self.on_interaction = ons["interaction"]
        self.on_register = ons["register"]
        self.register2 = ons["register2"]

        # Other
        self.isrunning = True
        self.isafk = False

        self.ws = None

        await self._runner()

    async def _runner(self):
        async with ClientSession() as s:
            async with s.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json") as ws:
                self.ws = ws

                j = await self.get_responce(ws)

                interval = j["d"]["heartbeat_interval"]

                from datetime import datetime
                from time import mktime

                await self.send_request({"op": 2, "d": {
                    "token": self.token,
                    "intents": self.intents,
                    "properties": {
                        "$os": "linux",
                        "$browser": "disspy",
                        "$device": "iphone"
                    },
                    "presence": {
                        "since": mktime(datetime.now().timetuple()) * 1000,
                        "afk": self.isafk,
                        "status": self.status,
                        "activities": [self.activity]
                    }
                }}, ws)

                del mktime, datetime

                self.isrunning = True

                await asyncio.wait(fs=[self.heartbeat(ws, interval / 1000), self._events_checker(ws)])

    async def heartbeat(self, ws, interval):
        while True:
            await self.send_request({"op": 1, "d": None, "t": None}, ws)

            await asyncio.sleep(interval)

    async def _events_checker(self, ws):
        while True:
            event_json = await self.get_responce(ws)
            event = _FlowEvent(event_json)

            if event.type == "READY":
                await self.register(event.data)
                await self.register2()
                await self.on_register()

                await self.on_ready()

            if event.type == "MESSAGE_CREATE":
                _m = DisMessage(event.data, self.token)

                if not event.data["author"]["id"] == self.user_id:
                    try:
                        await self.on_messagec(_m)
                    except TypeError:
                        pass

            if event.type == "INTERACTION_CREATE":
                if event.data["type"] == 2:
                    await self.on_interaction(event.data["token"], event.data["id"], event.data["data"]["name"],
                                              self.token, event.data["type"], event.data, event.data["data"]["type"])
                else:
                    await self.on_interaction(event.data["token"], event.data["id"], event.data["data"]["name"],
                                              self.token, event.data["type"], event.data, None)

            if event.type == "MESSAGE_REACTION_ADD":
                from disspy.reaction import DisEmoji, DisReaction
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

                await self.on_reaction(_r)

            if event.type == "MESSAGE_REACTION_REMOVE":
                from disspy.reaction import DisEmoji, DisRemovedReaction
                _m_id = int(event.data["message_id"])
                _c_id = int(event.data["channel_id"])
                _g_id = int(event.data["guild_id"])

                _e_json = event.data["emoji"]

                if _e_json["id"] is None:
                    _e = DisEmoji(unicode=_e_json["name"])
                else:
                    _e = DisEmoji(name=_e_json["name"], emoji_id=int(_e_json["id"]))

                _r = DisRemovedReaction(_m_id, _c_id, _g_id, _e, self.token)

                await self.on_reactionr(_r)

            if event.type == "TYPING_START":
                try:
                    if event.data["guild_id"]:
                        _u: DisUser = DisUser(event.data["member"]["user"], self.token)
                        _c: DisChannel = DisChannel(event.data["channel_id"], self.token)

                        await self.on_typing_start(_u, _c)
                    else:
                        _u_id = event.data["user_id"]
                        _u_json = Rest(self.token).get("user", _u_id)

                        _u: DisUser = DisUser(_u_json, self.token)
                        _c: DisDm = DisDm(event.data["channel_id"], self.token)

                        await self.on_dm_typing_start(_u, _c)
                except KeyError:
                    _u_id = event.data["user_id"]
                    _u_json = Rest(self.token).get("user", _u_id)

                    _u: DisUser = DisUser(_u_json, self.token)
                    _c: DisDm = DisDm(event.data["channel_id"], self.token)

                    await self.on_dm_typing_start(_u, _c)

            await asyncio.sleep(0.5)

    async def disconnecter(self):
        await self.ws.close()


@final
class DisApi(_RequestsUserClass):
    def __init__(self, token: str, intents, application_id):
        """
        Init Class
        -----
        :param token: Token of bot (from Discord Developer Portal)
        :param intents: Intents of bot
        :param application_id: Application Id of bot (from Discord Developer Portal)
        """
        super().__init__()

        self._headers = {'Authorization': f'Bot {token}', "content-type": "application/json"}
        self.app_commands_jsons = []

        self._on_ready = None
        self._on_messagec = None
        self.token = token
        self.application_id = application_id

        self.f = Flow(10, self.token, intents, {})
        self._r = Rest(self.token)

        self.app_commands = []
        self.raw_app_commands = []

        self.app_commands.append({})  # Slash Commands
        self.app_commands.append({})  # User Commands
        self.app_commands.append({})  # Message Commands

    def fetch(self, channel_id, message_id) -> DisMessage:
        _url = f"{_mainurl()}channels/{channel_id}/messages/{message_id}"

        _d = self._r.fetch(channel_id, message_id)

        return DisMessage(_d, self.token)

    async def run(self, status, ons: Dict[Text, Awaitable], debug: bool, act: Dict[str, Any]) -> NoReturn:
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

        _url = f"{_mainurl()}applications/{self.application_id}/commands"

        from requests import delete, post, get, patch

        _raws = get(_url, headers=self._headers).json()

        for r in _raws:
            for j in self.app_commands_jsons:
                if r["name"] == j["name"] and r["type"] == j["type"]:
                    _res = r

                    try:
                        _res["description"] = j["description"]
                    except KeyError:
                        pass

                    try:
                        _res["options"] = j["options"]
                    except KeyError:
                        pass

                    patch(f"{_url}/{r['id']}", json=j, headers=self._headers)
                else:
                    delete(f"{_url}/{r['id']}", headers=self._headers)
                    post(url=_url, json=j, headers=self._headers)

        del delete

        await self.f.run(ons, status, debug, act)

    async def disconnecter(self):
        await self.f.disconnecter()

    async def _on_messagec(self, message):
        pass

    async def _on_ready(self):
        pass

    async def _register2(self):
        # pass
        self.user: DisUser = self.get_user(self.f.user_id)

    async def _on_interaction(self, token, id, command_name, bot_token: str, type, data: JsonOutput, type_of_command: int = None):
        if type_of_command is None:
            return  # Not components!
        else:
            if type == 2:
                _ctx = Context(token, id, bot_token)

                try:
                    if type_of_command == 3:  # Message Commands
                        rs: dict = data["data"]["resolved"]["messages"]

                        _m_id = list(rs.keys())[0]
                        _m_d: dict = rs[_m_id]

                        try:
                            _m_d["id"] = _m_id
                        except KeyError:
                            _m_d.setdefault("id", _m_id)

                        _m = DisMessage(_m_d, self.token)

                        await self.app_commands[type_of_command - 1][command_name](_ctx, _m)

                    elif type_of_command == 2:  # User Commands
                        rs: dict = data["data"]["resolved"]["users"]

                        _u_id = list(rs.keys())[0]
                        _u_d: dict = rs[_u_id]

                        try:
                            _u_d["id"] = _u_id
                        except KeyError:
                            _u_d.setdefault("id", _u_id)

                        _u = DisUser(_u_d, self.token)

                        await self.app_commands[type_of_command - 1][command_name](_ctx, _u)

                    elif type_of_command == 1:  # Slash Commands
                        _args = []

                        from disspy.application_commands import _Argument, OptionArgs

                        try:
                            for o in data["data"]["options"]:
                                _args.append(_Argument(o["name"],
                                                       o["type"],
                                                       o["value"]))
                        except KeyError:
                            _args = []

                        await self.app_commands[type_of_command - 1][command_name](_ctx, OptionArgs(_args))
                    else:
                        pass
                except KeyError:
                    print("What! Application command is invalid")

    @overload
    async def send_message(self, id: int, content: str = "", embed: Optional[DisEmbed] = None):
        """
        Sending messages to channel
        -----
        :param id: Id of channel which use in sending messages to
        :param content: Message Content
        :param embed: Message Embed
        :return None:
        """

        if embed:
            await self._r.send_message(id, {"content": content, "embeds": [embed.tojson()]})
        else:
            await self._r.send_message(id, {"content": content})

    @overload
    async def send_message(self, id: int, content: str = "", embeds: Optional[list[DisEmbed]] = None):
        """
        Sending messages to channel
        -----
        :param id: Id of channel which use in sending messages to
        :param content: Message Content
        :param embeds: Message Embeds
        :return None:
        """

        embeds_send_jsons = []
        if embeds:
            for e in embeds:
                embeds_send_jsons.append(e.tojson())

            await self._r.send_message(id, {"content": content, "embeds": embeds_send_jsons})
        else:
            await self._r.send_message(id, {"content": content})

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
        user_id = int(user_id)  # If Showflake this will be int

        return self._r.get("user", user_id)

    def get_channel(self, channel_id: ChannelId) -> DisChannel:
        """
        Get channel by id
        -----
        :param channel_id: id of channel
        :return DisChannel:
        """
        channel_id = int(channel_id)  # If Showflake this will be int

        return DisChannel(channel_id, self)

    def get_channel_json(self, channel_id: ChannelId) -> JsonOutput:
        """
        Get channel by id (Json Output)
        -----
        :param channel_id: id of channel
        :return JsonOutput:
        """
        channel_id = int(channel_id)  # If Showflake this will be int

        return self._r.get("channel", channel_id)

    def get_guild(self, guild_id: GuildlId) -> DisGuild:
        """
        Get guild by id

        :param guild_id: id of guild
        :return DisGuild:
        """
        guild_id = int(guild_id)  # If Showflake this will be int

        return DisGuild(guild_id, self)

    def get_guild_json(self, guild_id: GuildlId) -> JsonOutput:
        """
        Get guild by id (Json Output)

        :param guild_id: id of guild
        :return JsonOutput:
        """

        guild_id = int(guild_id)  # If Showflake this will be int

        return self._r.get("guild", guild_id)

    def create_command(self, payload, func: Awaitable):
        _url = f"https://discord.com/api/v10/applications/{self.application_id}/commands"

        def app_func_register(number):
            self.app_commands[number][payload["name"]] = func

        if payload["type"] == 1:
            # Register interaction func to Slash Commands
            self.app_commands_jsons.append(payload)

            app_func_register(0)

        elif payload["type"] == 2:
            # Register interaction func to User Commands
            try:
                if payload["description"]:
                    self.app_commands_jsons.append(payload)

                    app_func_register(1)
            except KeyError:
                self.app_commands_jsons.append(payload)

                app_func_register(1)

        elif payload["type"] == 3:
            # Register interaction func to Message Commands
            try:
                if payload["description"]:
                    self.app_commands_jsons.append(payload)

                    app_func_register(2)
            except KeyError:
                self.app_commands_jsons.append(payload)

                app_func_register(2)

    async def fsend_request(self, data):
        await self.f.send_request(data, self.f.ws)
