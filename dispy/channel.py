import dispy.http.rest
from .embed import DisEmbed
from .message import DisMessage


class DisChannel:
    def __init__(self, data: dict, rest: dispy.http.rest.Rest):
        self._rest = rest
        self.id = data['id']
        self.last_message_id = data['last_message_id']
        self.guild_id = data["guild_id"]

    def __eq__(self, other):
        return self.id == other.id

    async def send(self, content: str = None, embeds: list[DisEmbed] = None, embed: DisEmbed = None):
        if embed is not None:
            await self._rest.send_message(self.id, {"content": content, "embeds": [embed.tojson()]})
        else:
            if embeds is not None:
                embeds_send_json = []

                for e in embeds:
                    embeds_send_json.append(e.tojson())

                await self._rest.send_message(self.id, {"content": content, "embeds": embeds_send_json})
            else:
                await self._rest.send_message(self.id, {"content": content})

    def fetch(self, id: int):
        return DisMessage(self._rest.fetch(self.id, id))
