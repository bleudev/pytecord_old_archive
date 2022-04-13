from channel import DisChannel


class DisMessage:
    def __init__(self, id, api, channel):
        self.id = id

        self.channel: DisChannel = channel
        _data = api.fetch(self.channel.id, self.id)

        self._api = api
