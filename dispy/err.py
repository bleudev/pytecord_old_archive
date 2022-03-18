class DisErr:
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Errors:
    DisBotInitErr = DisErr("b001", "Invalid prefix of bot")
    DisBotEventErr = DisErr("b002", "Ivalid event type")

    @staticmethod
    def raiseerr(obj: DisErr):
        raise RuntimeError(f"{obj.code} - {obj.message}")