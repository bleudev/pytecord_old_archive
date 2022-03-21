from .http.rest import Rest


class Channel:
    def __init__(self, data: dict, rest: Rest):
        self._rest = rest
        self.id = data['id']
        self.last_message_id = data['last_message_id']
        self.guild_id = data["guild_id"]

    async def send(self, content=None, embeds=None, embed=None):
        if embed is not None:
            await self._rest.send_message(self.id, {"content": content, "embeds": [embed]})
        else:
            await self._rest.send_message(self.id, {"content": content, "embeds": embeds})
