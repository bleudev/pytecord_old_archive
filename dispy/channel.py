import dispy.http.rest
from .embed import DisEmbed
from .message import DisMessage


class DisChannel:
    def __init__(self, data: dict, rest: dispy.http.rest.Rest):
        """
        Creating an object DisChannel

        :param data: dict -> data of the channel (json format)
        :param rest: Rest -> rest client with token for channel
        """
        self._rest = rest
        self.json = data
        self.id = data['id']
        self.last_message_id = data['last_message_id']
        self.guild_id = data["guild_id"]

    def __eq__(self, other):
        """
        __eq__ have using in "==" operator

        :param other: Other object (DisChannel)
        :return: bool -> if id of this object equals with id of other object :returns: True, else False:
        """
        return self.id == other.id

    async def send(self, content: str = None, embeds: list[DisEmbed] = None):
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embeds: list[DisEmbed] = None -> Embeds for message (DisEmbed - embed) (default is None)
        :return: None
        """

        embeds_send_json = []
        if embeds:
            for e in embeds:
                embeds_send_json.append(e.tojson())

            await self._rest.send_message(self.id, {"content": content, "embeds": embeds_send_json})
        else:
            await self._rest.send_message(self.id, {"content": content})

    async def send(self, content: str = None, embed: DisEmbed = None):
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embed: DisEmbed = None -> Embed for message (DisEmbed - embed) (default is None)
        :return: None
        """
        if embed:
            await self._rest.send_message(self.id, {"content": content, "embeds": [embed.tojson()]})
        else:
            await self._rest.send_message(self.id, {"content": content})

    def fetch(self, id: int):
        return DisMessage(self._rest.fetch(self.id, id), self._rest, self)


class DisDm:
    def __init__(self, data, rest):
        self._rest = rest
        self.id = data["id"]

    def fetch(self, id: int):
        return DisMessage(self._rest.fetch(self.id, id), self._rest)
