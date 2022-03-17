from api.http.rest import Rest

class Channel:
    def __init__(self, data: dict, rest: Rest):
        self._rest = rest
        self.id = data['id']
        self.last_message_id = data['last_message_id']
        self.guild_id = data["guild_id"]

    def send(self, text):
        self._rest.send_message(self.id, {"content": text})
