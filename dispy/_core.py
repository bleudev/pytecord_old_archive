import typing
import aiohttp
import requests
import asyncio
import threading
import time
import websocket
import json

from dispy import DisMessage, DisUser, DisChannel, DisGuild


class DisFlags:
    @staticmethod
    def default():
        return 512


class _Rest:
    def __init__(self, token):
        self.token = token
        self._s = aiohttp.ClientSession()

    def _headers(self):
        return {'Authorization': f'Bot {self.token}'}

    def get(self, goal: str, id: int):
        if goal.casefold() == 'guild':
            return requests.get(f'https://discord.com/api/v10/guilds/{str(id)}',
                                headers=self._headers()).json()
        elif goal.casefold() == 'channel':
            return requests.get(f'https://discord.com/api/v10/channels/{str(id)}',
                                headers=self._headers()).json()
        elif goal.casefold() == "user":
            return requests.get(f'https://discord.com/api/v10/users/{str(id)}',
                                headers=self._headers()).json()

    def fetch(self, channel_id, message_id):
        return requests.get(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages/{str(message_id)}',
                            headers=self._headers()).json()

    async def send_message(self, channel_id, post):
        await self._s.post(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages', json=post, headers=self._headers())


class _Gateway:
    def __init__(self, gateway_version: int, token: str, intents: int, activity: dict,
                 status: str, on_ready: typing.Awaitable, on_messagec: typing.Awaitable, register: typing.Awaitable,
                 on_register: typing.Awaitable):
        # Setting up connecting to Gateway
        self.gateway_version: int = gateway_version
        self.ws = websocket.WebSocket()
        self.intents = intents
        self.activity = activity
        self.status = status
        self.token = token
        self._rest = Rest(token)

        self.on_ready = on_ready
        self.on_messagec = on_messagec
        self.register = register
        self.on_register = on_register

    def run(self):
        # Connecting to Gateway
        self.ws.connect(f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json")

        # Parsing Opcode 10 Hello to Heartbeat Interval
        self.heartbeat_interval = self.get_responce()["d"]["heartbeat_interval"]

        # Setting up Opcode 1 Heartbeat
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.heartbeat_thread.start()

        # Sending Opcode 2 Identify
        self.send_opcode_2()

        self.heartbeat_thread.join()

    def send_request(self, json_data):
        self.ws.send(json.dumps(json_data))

    def get_responce(self):
        responce = self.ws.recv()
        return json.loads(responce)

    async def register(self, d):
        return

    def on_ready(self):
        return

    def on_messagec(self, message: DisMessage):
        return

    def on_register(self):
        return

    def heartbeat(self):
        while True:
            self.heartbeat_events_create()

            time.sleep(self.heartbeat_interval / 1000)

    def heartbeat_events_create(self):
        self.send_opcode_1()
        event = self.get_responce()
        self._check(event)

    def send_opcode_1(self):
        self.send_request({"op": 1, "d": "null"})

    def send_opcode_2(self):
        self.send_request({"op": 2, "d": {"token": self.token,
                                          "properties": {"$os": "linux", "$browser": "dispy", "$device": "dispy"},
                                          "presence": {"activities": [self.activity],
                                                       "status": self.status, "since": 91879201, "afk": False},
                                          "intents": self.intents}})

    def _check(self, event: dict):
        if event["t"] == "READY":
            asyncio.run(self.register(event["d"]))
            asyncio.run(self.on_ready())
            asyncio.run(self.on_register())
            self.user_id = event["d"]["user"]["id"]

        if event["t"] == "MESSAGE_CREATE":
            if self._check_notbot(event):
                _message_id = int(event["d"]["id"])
                _channel_id = int(event["d"]["channel_id"])

                channel = DisChannel(self._rest.get("channel", _channel_id), self._rest)
                asyncio.run(self.on_messagec(channel.fetch(_message_id)))

    def _check_notbot(self, event: dict) -> bool:
        return self.user_id != event["d"]["author"]["id"]


class DisApi:
    def __init__(self, token):
        self.token = token

        self._g = None
        self._r = _Rest(self.token)

    async def _on_ready(self):
        return

    def run(self, gateway_version: int, intents: int, status, on_ready: typing.Awaitable, on_messagec: typing.Awaitable, on_register: typing.Awaitable):
        if on_messagec is not None:
            self._on_message = on_messagec
        if on_ready is not None:
            self._on_ready = on_ready

        self._g = _Gateway(gateway_version, self.token, intents, {}, status, self._on_ready, self._on_message, self._register, on_register)
        self._g.run()

    async def _register(self, d):
        self.user: DisUser = self.get_user(d["user"]["id"], False)

    async def _on_message(self, message: DisMessage):
        return

    def get_user(self, id: int, premium_gets):
        return DisUser(id, self._r, premium_gets)

    def get_channel(self, id: int):
        return DisChannel(self._r.get('channel', id), self._r)

    def get_guild(self, id: int):
        return DisGuild(self._r.get('guild', id), self._r)
