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

# Typing imports
from typing import (
    Type,
    TypeVar,
    Awaitable,
    Union
)

import aiohttp
import requests

from disspy.application_commands import Context
from disspy.channel import DisChannel
from disspy.errs import ClassTypeError
from disspy.guild import DisGuild
# disspy imports
from disspy.message import DisMessage
from disspy.user import DisUser


class DisFlags:
    """
    The class for using intents in bots

    :methods:
        :method: default()
            Implements GUILD_MESSAGES and default intents
        :method: all()
            Implements all Gateway Intents
    """

    @staticmethod
    def default():
        return 512

    @staticmethod
    def all():
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


class _Rest:
    def __init__(self, token):
        self.token = token

    def _headers(self):
        return {'Authorization': f'Bot {self.token}'}

    def get(self, goal: str, id: Union[int, Showflake]) -> JsonOutput:
        """
        :param goal: guild/channel/user
        :param id: id of guild/channel/user
        :return JsonOutput: Json answer from Discord API server
        """
        id = int(id)

        if goal.casefold() == 'guild':
            return JsonOutput(kwargs=requests.get(f'https://discord.com/api/v10/guilds/{str(id)}',
                              headers=self._headers()).json())

        elif goal.casefold() == 'channel':
            return JsonOutput(kwargs=requests.get(f'https://discord.com/api/v10/channels/{str(id)}',
                              headers=self._headers()).json())

        elif goal.casefold() == "user":
            return JsonOutput(kwargs=requests.get(f'https://discord.com/api/v10/users/{str(id)}',
                              headers=self._headers()).json())

    def fetch(self, channel_id, message_id) -> JsonOutput:
        _channel_id, _message_id = [str(channel_id), str(message_id)]
        _1part = "https://discord.com/api/v10/channels/"
        _2part = f"{_channel_id}/messages/{_message_id}"
        return JsonOutput(kwargs=requests.get(f"{_1part}{_2part}",
                          headers=self._headers()).json())

    async def send_message(self, channel_id, post):
        async with aiohttp.ClientSession() as s:
            await s.post(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages', json=post,
                         headers=self._headers())


class _Gateway:
    def __init__(self, gateway_version: int, token: str, intents: int,
                 activity: dict):
        self.user_id = "null"
        self.heartbeat_interval = 0

        self.gateway_version: int = gateway_version
        self.session = aiohttp.ClientSession()

        self.intents = intents
        self.activity = activity

        self.token = token
        self._rest = _Rest(token)

    def run(self, on_ready: Awaitable, on_messagec: Awaitable, register2: Awaitable,
            on_register: Awaitable, status, on_interaction):
        self.status = status
        self.on_ready = on_ready
        self.on_messagec = on_messagec
        self.register2 = register2
        self.on_register = on_register
        self.on_interaction = on_interaction

        # Connecting to Gateway
        async with self.session.ws_connect(f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json") as ws:
            # Parsing Opcode 10 Hello to Heartbeat Interval
            self.heartbeat_interval = self.get_responce(ws)["d"]["heartbeat_interval"]

            # Setting up Opcode 1 Heartbeat
            asyncio.run(self.heartbeat(ws))

    async def send_request(self, json_data, ws):
        await ws.send_json(json_data)

    async def get_responce(self, ws):
        return json.loads(await ws.receive_json())

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

    async def on_interaction(self, token, id, command_id, bot_token: str):
        pass

    async def heartbeat(self, ws):
        # Sending Opcode 2 Identify
        await self.send_opcode_2(ws)
        while True:
            await self.heartbeat_events_create(ws)

            await asyncio.sleep(self.heartbeat_interval / 1000)

    async def heartbeat_events_create(self, ws):
        await self.send_opcode_1(ws)
        await self._check(await self.get_responce(ws))

    async def send_opcode_1(self, ws):
        await self.send_request({"op": 1, "d": "null"}, ws)

    async def send_opcode_2(self, ws):
        await self.send_request({"op": 2, "d": {"token": self.token,
                                          "properties": {"$os": "linux", "$browser": "dispy", "$device": "dispy"},
                                          "presence": {"activities": [self.activity],
                                                       "status": self.status, "since": 91879201, "afk": False},
                                          "intents": self.intents}}, ws)

    async def _check(self, event: dict):
        print(event)
        if event["t"] == "READY":
            await self.register(event["d"])
            await self.register2()
            try:
                asyncio.create_task(self.on_ready())
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

                asyncio.create_task(self.on_messagec(_message))

        if event["t"] == "INTERACTION_CREATE":
            _token = event["d"]["token"]
            _interactionid = event["d"]["id"]
            _commandid = event["d"]["data"]["id"]
            _token = self.token

            asyncio.create_task(self.on_interaction(_token, _interactionid, _commandid, _token))


class DisApi:
    def __init__(self, token, intents, application_id):
        self._on_ready = None
        self._on_messagec = None
        self.token = token
        self.application_id = application_id

        self.g = _Gateway(10, self.token, intents, {}, application_id)
        self._r = _Rest(self.token)

        self.slashs = {}

    def fetch(self, channel_id, id):
        return DisMessage(id, channel_id, DisApi(self.token))

    def run(self, status, on_ready: Awaitable, on_messagec: Awaitable,
            on_register: Awaitable):
        if on_messagec is not None:
            self._on_messagec = on_messagec
        if on_ready is not None:
            self._on_ready = on_ready

        self.g.run(self._on_ready, self._on_messagec, self._register2, on_register, status, self._on_interaction)

    async def _on_message(self, message):
        pass

    async def _on_ready(self):
        pass

    async def _register2(self):
        # pass
        self.user: DisUser = self.get_user(self.g.user_id, False)

    async def _on_interaction(self, token, id, command_id, bot_token: str):
        try:
            _ctx = Context(token, id, bot_token)

            asyncio.create_task(self.slashs[command_id](_ctx))
        except KeyError:
            print("What! Slash command is invalid")

    def _headers(self):
        return {'Authorization': f'Bot {self.token}'}

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

    def get_user(self, id: int, premium_gets) -> DisUser:
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
        return JsonOutput(kwargs=self._r.get("user", id))

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

        _s = requests.post(url=_url, headers=self._headers(), json=payload).json()

        self.slashs[_s["id"]] = func
