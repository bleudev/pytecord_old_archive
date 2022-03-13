import api.client


class DisBotType:
    commands = 1
    slash = 2
    chat_message = 3


class DisErr:
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Errors:
    DisBotInitErr = DisErr("b001", "Invalid type of bot")

    @staticmethod
    def raiseerr(obj: DisErr):
        raise RuntimeError(f"{obj.code} - {obj.message}")