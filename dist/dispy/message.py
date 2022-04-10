import dist.dispy.http.rest


class DisMessage:
    def __init__(self, data: dict, rest: dist.dispy.http.rest.Rest, channel):
        self.id = data["id"]
        self._rest = rest
        self.channel: dispy.DisChannel = channel
