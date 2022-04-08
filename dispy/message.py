import dispy.http.rest


class DisMessage:
    def __init__(self, data, rest: dispy.http.rest.Rest, channel):
        self.id = data["id"]
        self._rest = rest
        self.channel = channel
