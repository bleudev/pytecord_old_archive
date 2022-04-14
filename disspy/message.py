from .channel import DisChannel


class DisMessage:
    def __init__(self, id, channel_id, r):
        self.id = id
        self.channel_id = channel_id
        self._r = r
        self.channel = DisChannel(self.channel_id, self._r)

        _data = self._r.fetch(self.channel_id, self.id)
