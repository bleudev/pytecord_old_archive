from api import Errors as err
from api.http.rest import Rest

class DisBot:
    def __init__(self, token: str, prefix="!"):
        self._rest = Rest(token)
        if prefix == "" or " " in prefix:
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
