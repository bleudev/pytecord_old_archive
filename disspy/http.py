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
    Union,
    Coroutine,
    Callable,
    NewType,
    Dict,
    List,
    Text,
    Any,
    final,
    Literal,
)

from enum import Enum, auto
from aiohttp import ClientSession
from requests import delete, post, get
import colorama


# disspy imports
from disspy.channel import Channel, Message
from disspy.thread import DisNewsThread, DisThread, DisPrivateThread
from disspy.guild import Guild
from disspy.user import User
from disspy.app_commands import Context
from disspy.webhook import DispyWebhook

JsonOutput = NewType("JsonOutput", Dict[str, Any])

# __all__
__all__: tuple = (
    # Classes for simpler creating other classes
    "JsonOutput",
    "Flags",
    # Private clients
    "Rest",
    # Main client
    "DisApi",
)


def _mainurl() -> Literal["https://discord.com/api/v10/"]:
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
    DIRECT_MESSAGE_TYPING = auto()
    MESSAGE_CONTENT = auto()
    GUILD_SCHEDULED_EVENTS = auto()


def _value(*args):
    res = 0

    for i in list(args):
        res += int(i.value)

    return res


class Flags:
    """
    The class for using intents in bots

    # Methods

    `default()`
        Implements GUILD_MESSAGES and default intents

    `all()`
        Implements all Gateway Intents
    """

    def __all__(self) -> List[str]:
        return [str(self.default()), str(self.all())]

    def __type__(self) -> type:
        return int

    @staticmethod
    def default() -> int:
        """
        Implements:
            None

        :return int: integer value of intents
        """
        return _value(_Intents.GUILD_INTEGRATIONS)

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

        return _value(_Intents.GUILD_MESSAGE_TYPING,
                      _Intents.DIRECT_MESSAGE_TYPING,
                      _Intents.GUILD_MESSAGES,
                      _Intents.DIRECT_MESSAGES,
                      _Intents.MESSAGE_CONTENT,
                      _Intents.GUILD_INTEGRATIONS)

    @staticmethod
    def reactions() -> int:
        """
        Implements:
            1. GUILD_MESSAGE_REACTIONS
            2. DIRECT_MESSAGE_REACTIONS

        :return int: integer value of intents
        """

        return _value(_Intents.DIRECT_MESSAGE_REACTIONS,
                      _Intents.GUILD_MESSAGE_REACTIONS,
                      _Intents.GUILD_INTEGRATIONS)

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


@final
class Rest:
    """
    Rest class
    """

    __classname__: str = "Rest"

    def __init__(self, token: str):
        self._headers = {
            "Authorization": f"Bot {token}",
            "content-type": "application/json",
        }

        self.__slots__ = [self._headers]

    def get(self, goal: str, goal_id: int) -> Union[JsonOutput, None]:
        """
        :param goal: guild/channel/user
        :param id: id of guild/channel/user
        :return JsonOutput: Json answer from Discord API server
        """
        goal_id = int(goal_id)

        if goal.casefold() == "guild":
            _url = f"{_mainurl()}guilds/{str(goal_id)}"
            return get(url=_url, headers=self._headers).json()

        if goal.casefold() == "channel":
            _url = f"{_mainurl()}channels/{str(goal_id)}"

            return get(url=_url, headers=self._headers).json()

        if goal.casefold() == "user":
            _url = f"{_mainurl()}users/{str(goal_id)}"

            return get(url=_url, headers=self._headers).json()

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

    async def send_message(self, channel_id, json_post, session):
        """send_message
        Send messages in channels

        Args:
            channel_id (int): Channel id
            json_post (dict): Json data for send

        Returns:
            dict: Json output
        """
        _url = f"{_mainurl()}channels/{channel_id}/messages"

        async with session.post(_url, data=json_post) as post_process:
            j = await post_process.json()
            return j


@final
class DisApi:
    """DisApi
    Class for init Rest and DispyWebhook event and edit they
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
        self._headers = {
            "Authorization": f"Bot {token}",
            "content-type": "application/json",
        }
        self.app_commands_jsons = []

        self._on_ready = None
        self._on_messagec = None
        self.token = token

        self.hook = DispyWebhook(10, self.token, intents)
        self._r = Rest(self.token)
        self.session = None

        self.app_commands = []
        self.raw_app_commands = []

        self.user = None
        self._debug = False

        self.app_commands.append({})  # Slash Commands
        self.app_commands.append({})  # User Commands
        self.app_commands.append({})  # Message Commands

    def fetch(self, channel_id, message_id) -> Message:
        """fetch
        Fetch message by its id and channel id

        Args:
            channel_id (int): Channel id
            message_id (int): Message id

        Returns:
            Message: Fetched message
        """
        _url = f"{_mainurl()}channels/{channel_id}/messages/{message_id}"

        _d = self._r.fetch(channel_id, message_id)

        return Message(_d, self.token, self.session)

    async def run(
        self, status, ons: Dict[Text, Callable], debug: bool, act: Dict[str, Any]
    ) -> None:
        """
        Run the hook of DisApi or run the bot.
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

        self.session = ClientSession(headers=self._headers)

        try:
            await self.hook.run(ons, status, debug, act, self.session)
        except KeyboardInterrupt:
            raise
        finally:
            async with self.session:
                pass

    async def _register2(self, data: dict):
        # pass
        self.user: User = self.get_user(self.hook.user_id)

        if self._debug:
            print(
                f"{colorama.Fore.YELLOW}Registering application commands...{colorama.Fore.RESET}"
            )

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
                    print(
                        f"{colorama.Fore.BLUE}POST |{colorama.Fore.RESET} {post_event}"
                    )

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
                    print(
                        f"{colorama.Fore.BLUE}POST |{colorama.Fore.RESET} {post_event}"
                    )

        if self._debug:
            server_app_commands = get(_url, headers=self._headers).json()

            print(
                f"{colorama.Fore.YELLOW}Current commands on server: {colorama.Fore.RESET}",
                end="",
            )
            print(server_app_commands)
            print(f"{colorama.Fore.GREEN}Regsiter is completed!")

    async def _on_interaction(self, data) -> None:
        interaction_info = (data["token"], int(data["id"]))
        ctx = Context(interaction_info, self.token)
        command = data["data"]
        callback = self.app_commands[command["type"] - 1][command["name"]]

        async def no_options():
            await callback(ctx)

        async def options():
            values = {}

            for i in command["options"]:

                def append_arg(key, value):
                    values.setdefault(key, value)

                try:
                    append_arg(i["name"], i["value"])
                except KeyError:
                    pass

            await callback(ctx, **values)

        if command["type"] == 1:  # Slash command
            try:
                if command["options"]:
                    await options()
                else:
                    await no_options()
            except KeyError:
                await no_options()

        elif command["type"] == 2:  # User command
            target_id = command["target_id"]

            target_json = command["resolved"]["users"][target_id]

            target = User(target_json, self.token)

            await callback(ctx, target)

        elif command["type"] == 3:  # Message command
            target_id = command["target_id"]

            target_json = command["resolved"]["messages"][target_id]

            target = Message(target_json, self.token, self.session)

            await callback(ctx, target)

    async def _on_components(self, data):
        if data["data"]["component_type"] == 2:
            _ctx = Context((data["token"], data["id"]), self.token)
            await self.comsevs[data["data"]["custom_id"]](_ctx)

        if data["data"]["component_type"] == 3:
            _ctx = Context((data["token"], data["id"]), self.token)
            _vs = data["data"]["values"]
            await self.comsevs[data["data"]["custom_id"]](_ctx, _vs)

    async def _on_modal_sumbit(self, data):
        _ctx = Context((data["token"], data["id"]), self.token)
        coms = data["data"]["components"][0]["components"]
        _v = ""

        for i in coms:
            if i["custom_id"] == data["data"]["custom_id"]:
                _v = i["value"]

        await self.comsevs[data["data"]["custom_id"]](_ctx, _v)

    def get_user(self, user_id: int) -> User:
        """
        Get user by id
        -----
        :param user_id: id of user
        :return User: User
        """

        return User(self.get_user_json(user_id), self.token)

    def get_user_json(self, user_id: int) -> JsonOutput:
        """
        Get user by id (Json Output)
        -----
        :param user_id: id of user
        :return JsonOutput:
        """
        user_id = int(user_id)

        return self._r.get("user", user_id)

    def get_channel_or_thread(
        self, object_id: int
    ) -> Union[Channel, DisNewsThread, DisThread, DisPrivateThread]:
        """
        Get channel or thread

        Args:
            object_id (int): Id of channel or thread

        Returns:
            Channel
            DisNewsThread
            DisThread
            DisPrivateThread
        """
        j = self._r.get("channel", object_id)
        _type = j["type"]

        _threads_objs = {10: DisNewsThread, 11: DisThread, 12: DisPrivateThread}

        if _type in (0, 1):  # Basic Channels
            return Channel(j, self.token, self.session)

        if _type in (10, 11, 12):  # Threads
            return _threads_objs[_type](j, self.token, self.session)

        return None

    def get_channel_json(self, channel_id: int) -> JsonOutput:
        """
        Get channel by id (Json Output)
        -----
        :param channel_id: id of channel
        :return JsonOutput:
        """
        channel_id = int(channel_id)

        return self._r.get("channel", channel_id)

    def get_guild(self, guild_id: int) -> Guild:
        """
        Get guild by id

        :param guild_id: id of guild
        :return Guild:
        """
        guild_id = int(guild_id)
        data = self.get_guild_json(guild_id)

        return Guild(data, self.token, self.session)

    def get_guild_json(self, guild_id: int) -> JsonOutput:
        """
        Get guild by id (Json Output)

        :param guild_id: id of guild
        :return JsonOutput:
        """

        guild_id = int(guild_id)

        return self._r.get("guild", guild_id)

    def create_command(
        self, payload: dict, func: Callable[..., Coroutine[Any, Any, Any]]
    ):
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

        Send to DispyWebhook a json request

        Args:
            data (dict): Json data for sending request
        """
        await self.hook.send_request(data, self.hook.websocket)
