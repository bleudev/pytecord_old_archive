from api import Errors as Err
from api.http.rest import Rest
from api.channel import Channel


class DisBot:
    def __init__(self, token: str, prefix="!"):
        self._rest = Rest(token)
        if prefix == "" or " " in prefix:
            Err.raiseerr(Err.DisBotInitErr)
        else:
            self.prefix = prefix

    def event(self, type: str):
        def wrapper(func):
            if type == "messagecreate":
                self.on_message = func
            elif type == "ready":
                self.on_ready = func
            else:
                Err.raiseerr(Err.DisBotEventErr)

    def get_channel(self, id: int):
        return Channel(self._rest.get('channel', id), self._rest)
