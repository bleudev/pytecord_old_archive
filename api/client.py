import api
from api import Errors as err


class DisBot:
    def __init__(self, token: str, prefix="!"):
        self.token = token
        if prefix == "" or prefix.startswith(" "):
            err.raiseerr(err.DisBotInitErr)
        else:
            self.prefix = prefix

    def event(self, type: str):
        return