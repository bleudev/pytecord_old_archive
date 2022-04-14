from disspy.embed import DisEmbed
import disspy.message


class DisChannel:
    def __init__(self, id: int, rest):
        """
        Creating an object DisChannel

        :param id: dict -> id of the channel
        :param rest: Rest -> Rest client with token for channel
        """
        self._r = rest
        self.id = id

        _data = self._r.get("channel", id)

        self.last_message_id = _data['last_message_id']
        self.guild_id = _data["guild_id"]

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

        await self._r.send_message(self.id, content, embeds)

    async def send(self, content: str = None, embed: DisEmbed = None):
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embed: DisEmbed = None -> Embed for message (DisEmbed - embed) (default is None)
        :return: None
        """
        _payload = {}

        if embed:
            _payload = {
                "content": content,
                "embeds": [embed.tojson()]
            }
        else:
            _payload = {
                "content": content
            }

        await self._r.send_message(self.id, _payload)

    def fetch(self, id: int):
        return disspy.message.DisMessage(id, self.id, self._r)

class DisDm:
    def __init__(self, id, api):
        self._api = api
        self.id = id

    def fetch(self, id: int):
        return self._api.fetch(self.id, id)
