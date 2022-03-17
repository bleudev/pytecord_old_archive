from api import Errors as err
from api.http import rest

class DisBot:
    def __init__(self, token: str, prefix="!"):
        self.rest = rest.Rest(token)
        if prefix == "" or prefix.startswith(" "):
            err.raiseerr(err.DisBotInitErr)
        else:
            self.prefix = prefix

    def event(self, type: str):
        def wrapper(func):
            if type == "messagecreate":
                self.on_message = func
            elif type == "ready":
                self.on_ready = func
            else:
                err.raiseerr(err.DisBotEventErr)