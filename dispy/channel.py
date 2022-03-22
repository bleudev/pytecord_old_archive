from .http.rest import Rest
from .embed import DisEmbed

class Channel:
    def __init__(self, data: dict, rest: Rest):
        self._rest = rest
        self.id = data['id']
        self.last_message_id = data['last_message_id']
        self.guild_id = data["guild_id"]

    async def send(self, content: str = None, embeds: list[DisEmbed] = None, embed: DisEmbed = None):
        if embed is not None:
            await self._rest.send_message(self.id, {"content": content, "embeds": [embed.tojson()]})
        else:
            embeds_send_json = []

            for e in embeds:
                embeds_send_json.append(e.tojson())

            await self._rest.send_message(self.id, {"content": content, "embeds": embeds_send_json})
