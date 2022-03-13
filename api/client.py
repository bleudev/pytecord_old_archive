import api
from api import Errors as err


class DisBot:
    def __init__(self, token: str, type: int=api.DisBotType.commands, prefix="!"):
        self.token = token
        self.type = type
        if type == 1:
            return DisBotCommands(token, prefix)

        elif type == 2:
            return DisBotSlash(token)
        elif type == 3:
            return DisBotChatMessage(token)
        else:
            err.raiseerr(err.DisBotInitErr)


class DisBotCommands(DisBot):
    def __init__(self, token, prefix):
        super(DisBotCommands, self).__init__(token, api.DisBotType.commands)
        self.prefix = prefix


class DisBotSlash(DisBot):
    def __init__(self, token):
        super(DisBotSlash, self).__init__(token, api.DisBotType.slash)


class DisBotChatMessage(DisBot):
    def __init__(self, token):
        super(DisBotChatMessage, self).__init__(token, api.DisBotType.chat_message)