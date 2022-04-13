import disspy.https as htt


class DisMessage:
    def __init__(self, data: dict, rest: htt.Rest, channel):
        self.id = data["id"]
        self._rest = rest
        self.channel: dispy.DisChannel = channel
