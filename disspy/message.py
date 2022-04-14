class DisMessage:
    def __init__(self, id, channel_id, api):
        self.id = id
        self.channel_id = channel_id

        _data = api.fetch(self.channel_id, self.id)

        self._api = api
