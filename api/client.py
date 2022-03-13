from api import DisBotType


class DisBot:
    def __init__(self, token, type):
        self.token = token
        self.type = type
        if type == 1


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