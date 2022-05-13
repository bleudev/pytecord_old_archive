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

# pckages imports
import asyncio
import json

from aiohttp import ClientSession
from requests import get, post, Response

# Typing imports
from typing import (
    Type,
    TypeVar,
    Awaitable,
    Union
)


from disspy.application_commands import Context
from disspy.channel import DisChannel
from disspy.errs import ClassTypeError
from disspy.guild import DisGuild
# disspy imports
from disspy.message import DisMessage
from disspy.user import DisUser
import colorama

__name__: str = "core"

__package__: str = "disspy"

__all__: tuple = (
    # Classes for simpler creating other classes
    "_RequestsUserClass",
    "DisFlags",
    "JsonOutput",
    "Showflake",
    # Private clients
    "_Rest",
    "_Gateway",
    # Main client
    "DisApi"
)

_fall = __all__


def _mainurl() -> str:
        return "https://discord.com/api/v10/"


""" Debuging classes """
colorama.init()


class _DebugLoggingWebsocket:
    def __new__(cls, *args, **kwargs):
        _data = args[0]

        try:
            _send = kwargs["send"]
        except KeyError:
            _send = False

        try:
            _isevent = kwargs["isevent"]
        except KeyError:
            _isevent = False

        _result = ""

        if _send:
            _result = f"{colorama.Fore.GREEN}Sending Request:{colorama.Fore.RESET} {_data}"
        else:
            if _isevent:
                _result = f"{colorama.Fore.RED}Getting Responce (Event):{colorama.Fore.RESET} {_data}"
            else:
                _result = f"{colorama.Fore.RED}Getting Responce:{colorama.Fore.RESET} {_data}"

        return _result


class _RequestsUserClass:
    async def _aiopost(self, url, data, headers):
        async with ClientSession(headers=headers) as _s:
            async with _s.post(url=url, data=data) as _p:
                return _p.json()

    def _post(self, url: str, data: dict, headers: dict) -> dict:
        return post(url=url, json=data, headers=headers).json()

    def _get(self, url: str, headers: dict) -> Response:
        return get(url=url, headers=headers)


class DisFlags:
    """
    The class for using intents in bots

    :methods:
        :method: default()
            Implements GUILD_MESSAGES and default intents
        :method: all()
            Implements all Gateway Intents
    """
    _numeral_of_class = 1

    _T = TypeVar(_fall[_numeral_of_class])

    @property
    def __class__(self) -> Type[_T]:
        return self._T

    def __all__(self):
        return [str(self.default()), str(self.all())]

    @staticmethod
    def default() -> int:
        return 512

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
                10. GUILD_MESSAGES (Privileged intent)
                11. GUILD_MESSAGE_REACTIONS
                12. GUILD_MESSAGE_TYPING
                13. DIRECT_MESSAGES
                14. DIRECT_MESSAGE_REACTIONS
                15. DIRECT_MESSAGE_TYPING
                16. GUILD_SCHEDULED_EVENTS

            :return: int (integer value of intents)
        """
        return 98303


class JsonOutput(dict):
    _T = TypeVar("JsonOutput")

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    @property
    def __class__(self: _T) -> Type[_T]:
        return self._T


class Showflake:
    """
Class info

Showflake is using for simpled work with tokens and ids.

Atributies:
    :var self.isid:
    """
    def __init__(self, value: str):
        if value.isdigit():
            self.isid = True
            self.istoken = False
            self.value = int(value)
        else:
            self.isid = False
            self.istoken = True
            self.value = value

    def __int__(self):
        if not self.isid:
            raise ClassTypeError("Class Value is str, but this method needs for int!")
        else:
            return int(self.value)

    def __str__(self):
        if not self.istoken:
            raise ClassTypeError("Class Value is int, but this method needs for str!")
        else:
            return str(self.value)


class _Rest(_RequestsUserClass):
    _T = TypeVar("_Rest")

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
            return JsonOutput(kwargs=get(f'{_mainurl()}guilds/{str(id)}',
                              headers=self._headers).json())

        elif goal.casefold() == 'channel':
            return JsonOutput(kwargs=get(f'https://discord.com/api/v10/channels/{str(id)}',
                              headers=self._headers).json())

        elif goal.casefold() == "user":
            _url = f'https://discord.com/api/v10/users/{str(id)}'

            return super()._get(_url, self._headers)

    def fetch(self, channel_id, message_id) -> JsonOutput:
        _channel_id, _message_id = [str(channel_id), str(message_id)]

        _url = f"{_mainurl()}channels/{_channel_id}/messages/{_message_id}"
        return super()._get(_url, super()._headers).json()

    async def send_message(self, channel_id, json_post):
        _url = f"{_mainurl()}channels/{channel_id}/messages"

        await super()._aiopost(_url, json_post, self._headers)


class _Gateway:
    def __init__(self, gateway_version: int, token: str, intents: int,
                 activity: dict):
        self.user_id = "null"
        self.heartbeat_interval = 0

        self.gateway_version: int = gateway_version

        self.intents = intents
        self.activity = activity

        self.token = token
        self._rest = _Rest(token)

        self._headers = {"content-type": "application/json"}

    async def run(self, on_ready: Awaitable, on_messagec: Awaitable, register2: Awaitable,
            on_register: Awaitable, status, on_interaction, debug):
        self.status = status
        self.on_ready = on_ready
        self.on_messagec = on_messagec
        self.register2 = register2
        self.on_register = on_register
        self.on_interaction = on_interaction

        self._debug = debug

        # Connecting to Gateway
        async with ClientSession(headers=self._headers) as session:
            async with session.ws_connect(f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json") as ws:
                # Parsing Opcode 10 Hello to Heartbeat Interval
                r = await self.get_responce(ws)
                if self._debug:
                    print(_DebugLoggingWebsocket(r, send=False))

                self.heartbeat_interval = r["d"]["heartbeat_interval"]

                # Setting up Opcode 1 Heartbeat
                await self.heartbeat(ws)

    async def send_request(self, json_data, ws):
        if self._debug:
            print(_DebugLoggingWebsocket(json_data, send=True))

        s = json.dumps(json_data).encode("utf-8")
        j2 = json.loads(s.decode("utf-8"))
        assert (json_data == j2)

        await ws.send_bytes(s)

    async def get_responce(self, ws):
        s = await ws.receive_str()

        return json.loads(s)

    async def register(self, d):
        self.user_id = d["user"]["id"]

    async def register2(self):
        pass

    async def on_ready(self):
        pass

    async def on_messagec(self, message: DisMessage):
        pass

    async def on_register(self):
        pass

    async def on_interaction(self, token, id, command_name, bot_token: str, type):
        pass

    async def heartbeat(self, ws):
        _isheartbeated = False

        # Sending Opcode 2 Identify
        await self.send_request({"op": 2, "d": {"token": self.token,
                                                "properties": {"$os": "linux", "$browser": "dispy", "$device": "dispy"},
                                                "presence": {"activities": [self.activity],
                                                             "status": self.status, "since": 91879201, "afk": False},
                                                "intents": self.intents}}, ws)
        while True:
            # Sending Opcode 1
            await self.send_request({"op": 1, "d": "null"}, ws)

            from asyncio import sleep
            from random import random

            # Check events
            event = await self.get_responce(ws)

            if self._debug:
                if event["t"] is None:
                    print(_DebugLoggingWebsocket(event, send=False, isevent=False))
                else:
                    print(_DebugLoggingWebsocket(event, send=False, isevent=True))

            if event["t"] == "READY":
                await self.register(event["d"])
                await self.register2()
                try:
                    await self.on_ready()

                except TypeError:
                    async def on_ready():
                        pass

                    await on_ready()

                await self.on_register()

            if event["t"] == "MESSAGE_CREATE":
                if self.user_id != event["d"]["author"]["id"]:
                    _message_id = int(event["d"]["id"])
                    _channel_id = int(event["d"]["channel_id"])

                    _channel = DisChannel(_channel_id, self._rest)
                    _message = _channel.fetch(_message_id)

                    await self.on_messagec(_message)

            if event["t"] == "INTERACTION_CREATE":
                _token = event["d"]["token"]
                _interactionid = event["d"]["id"]
                _commandname = event["d"]["data"]["name"]
                _type = event["d"]["type"]
                _token = self.token

                await self.on_interaction(_token, _interactionid, _commandname, _token, _type)

            if not _isheartbeated:
                await sleep((self.heartbeat_interval * random()) / 1000)
                _isheartbeated = True
            else:
                await sleep(self.heartbeat_interval / 1000)


class DisApi(_RequestsUserClass):
    def __init__(self, token: str, intents, application_id):
        super().__init__()

        self._headers = {'Authorization': f'Bot {token}', "content-type": "application/json"}

        self._on_ready = None
        self._on_messagec = None
        self.token = token
        self.application_id = application_id

        self.g = _Gateway(10, self.token, intents, {})
        self._r = _Rest(self.token)

        self.app_commands = []

        self.app_commands.append({}) # Slash Commands
        self.app_commands.append({}) # User Commands
        self.app_commands.append({}) # Message Commands

    def fetch(self, channel_id, id):
        return DisMessage(id, channel_id, DisApi(self.token))

    async def run(self, status, on_ready: Awaitable, on_messagec: Awaitable,
                  on_register: Awaitable, debug):
        if on_messagec is not None:
            self._on_messagec = on_messagec
        if on_ready is not None:
            self._on_ready = on_ready

        async with ClientSession(headers=self._headers) as s:
            _url = f"https://discord.com/api/v10/applications/{self.application_id}/commands"

            async with s.put(url=_url, data={}) as d:
                print(await d.json())

        await self.g.run(self._on_ready, self._on_messagec, self._register2, on_register, status, self._on_interaction, debug)

    async def _on_message(self, message):
        pass

    async def _on_ready(self):
        pass

    async def _register2(self):
        # pass
        self.user: DisUser = self.get_user(self.g.user_id, False)

    async def _on_interaction(self, token, id, command_name, bot_token: str, type):
        try:
            _ctx = Context(token, id, bot_token)

            await self.app_commands[type-1][command_name](_ctx)
        except KeyError:
            print("What! Slash command is invalid")

    async def send_message(self, id, content, embed):
        if embed:
            await self._r.send_message(id, {"content": content, "embeds": [embed.tojson()]})
        else:
            await self._r.send_message(id, {"content": content})

    async def send_message(self, id, content, embeds):
        embeds_send_json = []
        if embeds:
            for e in embeds:
                embeds_send_json.append(e.tojson())

            await self._r.send_message(id, {"content": content, "embeds": embeds_send_json})
        else:
            await self._r.send_message(id, {"content": content})

    def get_user(self, id: int, premium_gets: bool) -> DisUser:
        """
        Get user by id

        :param id: id of user
        :return DisUser:
        """
        return DisUser(id, self, premium_gets)

    def get_user_json(self, id: int) -> JsonOutput:
        """
        Get user by id (Json Output)

        :param id: id of user
        :return JsonOutput:
        """
        return self._r.get("user", id)

    def get_channel(self, id: Union[int, Showflake]) -> DisChannel:
        """
        Get channel by id

        :param id: id of channel
        :return DisChannel:
        """
        id = int(id)

        return DisChannel(id, DisApi(self.token))

    def get_channel_json(self, id: Union[int, Showflake]) -> JsonOutput:
        """
        Get channel by id (Json Output)

        :param id: id of channel
        :return JsonOutput:
        """
        return JsonOutput(kwargs=self._r.get("channel", id))

    def get_guild(self, id: Union[int, Showflake]) -> DisGuild:
        """
        Get guild by id

        :param id: id of guild
        :return DisGuild:
        """
        id = int(id)

        return DisGuild(id, DisApi(self.token))

    def get_guild_json(self, id: int) -> JsonOutput:
        """
        Get guild by id (Json Output)

        :param id: id of guild
        :return JsonOutput:
        """

        return JsonOutput(kwargs=self._r.get("guild", id))

    def create_command(self, payload, func):
        _url = f"https://discord.com/api/v10/applications/{self.application_id}/commands"



        def app_func_register(number):
            self.app_commands[number][payload["name"]] = func

        if payload["type"] == 1:
            # Register interaction func to Slash Commands
            _slash = post(_url, json=payload, headers=self._headers).json()

            app_func_register(0)

        elif payload["type"] == 2:
            # Register interaction func to User Commands
            try:
                if payload["description"] == "":

                    _slash = post(_url, json=payload, headers=self._headers).json()

                    app_func_register(1)
            except KeyError:
                _slash = post(_url, json=payload, headers=self._headers).json()

                app_func_register(1)

                return _slash

        elif payload["type"] == 3:
            # Register interaction func to Message Commands
            try:
                if payload["description"] == "":
                    _slash = post(_url, json=payload, headers=self._headers).json()

                    app_func_register(2)

                    return _slash
            except KeyError:
                _slash = post(_url, json=payload, headers=self._headers).json()

                app_func_register(2)

                return _slash
