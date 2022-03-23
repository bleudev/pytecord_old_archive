import asyncio
import dispy.http.rest

from .err import Errors as Err
from .channel import DisChannel
from .guild import DisGuild


class DisBot:
    def __init__(self, token: str, prefix="!"):
        self._rest = dispy.http.rest.Rest(token)
        self.isready = False
        if prefix == "" or " " in prefix:
            Err.raiseerr(Err.DisBotInitErr)
        else:
            self.prefix = prefix

    async def on_ready(self):
        return

    def on_message(self, message):
        return

    def on(self, type: str):
        def wrapper(func):
            if type == "messagecreate":
                self.on_message = func
            elif type == "ready":
                self.on_ready = func
            else:
                print("Error in on() - Invalid type of event (read docs)")

    def run(self):
        self.isready = True

        async def loop():
            if self.isready:
                asyncio.run(self.on_ready())

        asyncio.run(loop())

    def get_channel(self, id: int):
        return DisChannel(self._rest.get('channel', id), self._rest)

    def get_guild(self, id: int):
        return DisGuild(self._rest.get('guild', id), self._rest)
