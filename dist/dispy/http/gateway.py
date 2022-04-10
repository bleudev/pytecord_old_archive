import asyncio
import json
import threading
import time
import typing
import websocket

import dist.dispy.http.rest

class Gateway:
    def __init__(self, gateway_version: int, token: str, intents: int, activity: dict, status: str, on_ready: typing.Awaitable, on_message: typing.Awaitable, register: typing.Awaitable):
        # Setting up connecting to Gateway
        self.gateway_version: int = gateway_version
        self.ws = websocket.WebSocket()
        self.intents = intents
        self.activity = activity
        self.status = status
        self.token = token
        self._rest = dist.dispy.http.rest.Rest(token)

        self.on_ready = on_ready
        self.on_message = on_message
        self.register = register

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

    def on_message(self, message: dist.dispy.message.DisMessage):
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
            self.user_id = event["d"]["user"]["id"]

        if event["t"] == "MESSAGE_CREATE":
            if self._check_notbot(event):
                _message_id = int(event["d"]["id"])
                _channel_id = int(event["d"]["channel_id"])

                channel = dist.dispy.channel.DisChannel(self._rest.get("channel", _channel_id), self._rest)
                asyncio.run(self.on_message(channel.fetch(_message_id)))

    def _check_notbot(self, event: dict) -> bool:
        return self.user_id != event["d"]["author"]["id"]
