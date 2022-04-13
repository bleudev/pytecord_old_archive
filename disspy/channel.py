from disspy.embed import DisEmbed


class DisChannel:
    def __init__(self, id: int, api):
        """
        Creating an object DisChannel

        :param id: dict -> id of the channel
        :param api: Rest -> Api client with token for channel
        """
        self._api = api
        self.id = id

        _data = api.get_channel(id)

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

        await self._api.send_message(self.id, content, embeds)

    async def send(self, content: str = None, embed: DisEmbed = None):
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embed: DisEmbed = None -> Embed for message (DisEmbed - embed) (default is None)
        :return: None
        """
        await self._api.send_message(self.id, content, embed)

    def fetch(self, id: int):
        return self._api.fetch(self.id, id)


class DisDm:
    def __init__(self, id, api):
        self._api = api
        self.id = id

    def fetch(self, id: int):
        return self._api.fetch(self.id, id)
