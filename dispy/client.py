from dispy.http.rest import Rest
import dispy.errs as errs

from .channel import DisChannel
from .guild import DisGuild
from .embed import DisEmbed
from typing import *
from .http.gateway import Gateway
from dispy import DisBotType

__all__ = (
    "class DisBot"
)


class _BaseBot:
    _SLASH: str = "slash"
    _MESSAGE: str = "message"
    _COMMAND: str = "command"

    def __init__(self, token: str, type: Union[str, DisBotType], prefix: Optional[str] = "!"):
        self.token = token
        self.type = type
        self.prefix = prefix


class DisBot(_BaseBot):
    def __init__(self, token: str, prefix: Optional[str] = "!"):
        """
        Create bot

        :param token: str -> Discord Developers Portal Bot Token
        :param prefix: -> Prefix for bot
        """
        super().__init__()

        self._rest = Rest(token)

        self.isready = False
        if prefix == "" or " " in prefix:
            raise errs.PrefixError("Invalid prefix")
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

    # def run(self):
    #     self.isready = True
    #
    #     Gateway(10, self._rest.token, 512, {}, "online", self.on_ready, self.on_message)

    async def send(self, id: int, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        if self.isready:
            channel = self.get_channel(id)
            await channel.send(content=content, embeds=embeds)
        else:
            raise errs.SendError("Bot is not ready!")

    async def send(self, id: int, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        if self.isready:
            channel = self.get_channel(id)
            await channel.send(content=content, embed=embed)
        else:
            raise errs.SendError("Bot is not ready!")

    def get_channel(self, id: int):
        return DisChannel(self._rest.get('channel', id), self._rest)

    def get_guild(self, id: int):
        return DisGuild(self._rest.get('guild', id), self._rest)
