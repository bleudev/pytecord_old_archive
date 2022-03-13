from api import DisBotType
from api import Errors as err


class DisBot:
    def __init__(self, token, type, prefix=None):
        self.token = token
        self.type = type
        if type == 1:
            if prefix != None:
                return DisBotCommands(token, prefix)
            else:
                err.raiseerr(err.DisBotInitErr)
        elif type == 2:
            return DisBotSlash(token)
        elif type == 3:
            return DisBotChatMessage(token)


class DisBotCommands(DisBot):
    def __init__(self, token, prefix):
        super(DisBotCommands, self).__init__(token, DisBotType.commands)
        self.prefix = prefix


class DisBotSlash(DisBot):
    def __init__(self, token):
        super(DisBotSlash, self).__init__(token, DisBotType.slash)


class DisBotChatMessage(DisBot):
    def __init__(self, token):
        super(DisBotChatMessage, self).__init__(token, DisBotType.chat_message)