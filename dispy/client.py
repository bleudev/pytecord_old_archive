import asyncio

from .err import Errors as Err
from .http.rest import Rest
from .channel import Channel


class DisBot:
    def __init__(self, token: str, prefix="!"):
        self._rest = Rest(token)
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
        return Channel(self._rest.get('channel', id), self._rest)
