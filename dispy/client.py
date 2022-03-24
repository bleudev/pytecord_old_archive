import asyncio
import dispy.http.rest
import dispy.http.gateway

from .err import Errors as Err
from .channel import DisChannel
from .guild import DisGuild
from typing import *


class DisBot:
    def __init__(self, token: str, prefix: Optional[str]="!"):
        """
        Create bot

        :param token: str -> Discord Developers Portal Bot Token
        :param prefix: -> Prefix for bot
        """
        self._rest = dispy.http.Rest(token)
        self._gateway = dispy.http.Gateway(self._rest)

        self.isready = False
        if prefix == "" or " " in prefix:
            Err.raiseerr(Err.DisBotInitErr)
        else:
            self.prefix = prefix

    async def on_ready(self):
        return

    def on_message(self, message):
        return

    async def mainloop(self):
        while True:
            if self.isready:
                continue
                # Main settings
            else:
                continue

    def on(self, type: str):
        def wrapper(func):
            if type == "messagecreate":
                self.on_message = func
            elif type == "ready":
                self.on_ready = func
            else:
                print("Error in on() - Invalid type of event (read docs)")
        return wrapper

    def run(self):
        self.isready = True

        asyncio.run(self.on_ready())
        asyncio.run(self.mainloop())

    def get_channel(self, id: int):
        return DisChannel(self._rest.get('channel', id), self._rest)

    def get_guild(self, id: int):
        return DisGuild(self._rest.get('guild', id), self._rest)
