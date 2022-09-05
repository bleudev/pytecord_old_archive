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
# Packages
from typing import (
    TypeVar,
    Union,
    Coroutine,
    Callable,
    NewType,
    Dict,
    List,
    NoReturn,
    Text,
    Any,
    Generic,
    final
)

from enum import Enum, auto
from aiohttp import ClientSession
from requests import delete, post, get
import colorama


# disspy imports
from disspy.channel import (
    DisChannel,
    DisDmChannel,
    DisMessage,
    DmMessage
)
from disspy.thread import (
    DisNewsThread,
    DisThread,
    DisPrivateThread
)
from disspy.errors import ClassTypeError
from disspy.guild import DisGuild
from disspy.user import DisUser
from disspy.application_commands import Context, _Argument, OptionArgs
from disspy.webhook import DispyWebhook

JsonOutput = NewType("JsonOutput", Dict[str, Any])

# __all__
__all__: tuple = (
    # Classes for simpler creating other classes
    "JsonOutput",
    "DisFlags",
    "Snowflake",
    "ChannelId",
    "ThreadId",
    "UserId",
    "GuildId",
    # Private clients
    "Rest",
    # Main client
    "DisApi"
)

def _mainurl() -> str:
    return "https://discord.com/api/v10/"


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
ThreadId = NewType("ThreadId", int)
UserId = NewType("UserId", int)
GuildId = NewType("GuildId", int)


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
class DisApi:
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

        self.flow = DispyWebhook(10, self.token, intents)
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

            print(f"{colorama.Fore.YELLOW}Current commands on server: {colorama.Fore.RESET}",
                  end="")
            print(server_app_commands)
            print(f"{colorama.Fore.GREEN}Regsiter is completed!")

    async def _on_interaction(self, token, interaction_id, command_name, bot_token: str,
                              interaction_type, data: JsonOutput, type_of_command=None) -> NoReturn:
        interaction_info = (token, interaction_id)

        if interaction_type == 2:
            try:
                if type_of_command == 3:  # Message Commands
                    resolved: dict = data["data"]["resolved"]["messages"]

                    _m_id = list(resolved.keys())[0]
                    _m_d: dict = resolved[_m_id]

                    try:
                        _m_d["id"] = _m_id
                    except KeyError:
                        _m_d.setdefault("id", _m_id)

                    _c_id = _m_d["channel_id"]

                    _c_d = get(f"{_mainurl()}channels/{str(_c_id)}")

                    _m = None

                    if _c_d["type"] == 1:
                        _m = DisMessage(_m_d, self.token)
                    else:
                        _m = DmMessage(_m_d, self.token)

                    _ctx = Context(interaction_info, bot_token)
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

                    _ctx = Context(interaction_info, bot_token)
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

                    _ctx = Context(interaction_info, bot_token, OptionArgs(_args))

                    await func(_ctx)
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

    def get_channel_or_thread(self, object_id: int) -> Union[DisChannel, DisDmChannel,
                                                             DisNewsThread, DisThread,
                                                             DisPrivateThread]:
        """
        Get channel by id
        -----
        :param channel_id: id of channel
        :return DisChannel:
        """
        j = self._r.get("channel", object_id)
        _type = j["type"]

        _threads_objs = {
            10: DisNewsThread,
            11: DisThread,
            12: DisPrivateThread
        }

        if _type == 1:  # Dm Channels
            return DisDmChannel(object_id, self.token)

        if _type in [10, 11, 12]:  # Threads
            return _threads_objs[_type](j, self.token)

        return DisChannel(object_id, self.token)

    def get_channel_json(self, channel_id: ChannelId) -> JsonOutput:
        """
        Get channel by id (Json Output)
        -----
        :param channel_id: id of channel
        :return JsonOutput:
        """
        channel_id = int(channel_id)  # If Snowflake this will be int

        return self._r.get("channel", channel_id)

    def get_guild(self, guild_id: GuildId) -> DisGuild:
        """
        Get guild by id

        :param guild_id: id of guild
        :return DisGuild:
        """
        guild_id = int(guild_id)  # If Snowflake this will be int

        return DisGuild(guild_id, self.token)

    def get_guild_json(self, guild_id: GuildId) -> JsonOutput:
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
