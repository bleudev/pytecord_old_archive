"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from disspy.embed import DisEmbed
from disspy.message import DisMessage
from disspy.guild import DisGuild
from disspy.jsongenerators import _EmbedGenerator
from disspy.ui import ActionRow

from typing import (
    Optional,
    Union
)

__all__: tuple[str] = (
    "DisChannel",
    "DisDmChannel"
)


class _SendingRestHandler:
    @staticmethod
    async def execute(id, payload, token):
        from aiohttp import ClientSession as CS
        from json import dumps

        async with CS(headers={'Authorization': f'Bot {token}', 'content-type': 'application/json'}) as s:
            _u = f"https://discord.com/api/v9/channels/{id}/messages"

            async with s.post(_u, data=dumps(payload)) as p:
                j = await p.json()

                return j

    @staticmethod
    async def delete_channel(url, token):
        from aiohttp import ClientSession

        async with ClientSession(headers={'Authorization': f'Bot {token}', 'content-type': 'application/json'}) as s:
            await s.delete(url=url)


class _GettingChannelData:
    @staticmethod
    def execute(id, token):
        from requests import get

        _u = f"https://discord.com/api/v9/channels/{id}"
        _h = {'Authorization': f'Bot {token}'}

        return get(_u, headers=_h).json()

    @staticmethod
    def fetch(id, token, message_id):
        from requests import get

        _u = f"https://discord.com/api/v9/channels/{id}/messages/{message_id}"
        _h = {'Authorization': f'Bot {token}'}

        return get(_u, headers=_h).json()


class _GettingGuildData:
    @staticmethod
    def execute(id, token):
        from requests import get

        _u = f"https://discord.com/api/v9/guilds/{id}"
        _h = {'Authorization': f'Bot {token}'}

        return get(_u, headers=_h).json()


class DisChannel:
    """
    The class for sending messages to discord channels and fetching messages in channels
    """
    def __init__(self, id: int, _token):
        """
        Creating an object DisChannel

        :param id: dict -> id of the channel
        :param rest: Rest -> Rest client with token for channel
        """
        self._t = _token
        self.id = id

        _data = _GettingChannelData.execute(self.id, self._t)

        try:
            g_id = _data["guild_id"]

            _d = _GettingGuildData.execute(g_id, self._t)

            self.guild = DisGuild(_d, self._t)
        except KeyError:
            pass

    def __eq__(self, other):
        """
        __eq__ have using in "==" operator

        :param other: Other object (DisChannel)
        :return: bool -> if id of this object equals with id of other object :returns: True, else False:
        """
        return self.id == other.id

    async def send(self, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None, action_row: Optional[ActionRow] = None) -> Union[DisMessage, None]:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embeds: list[DisEmbed] = None -> Embeds for message (DisEmbed - embed) (default is None)
        :param action_row: ActionRow = None -> Action Row with components (default is None)
        :return DisMessage: Message which was sended
        """
        _payload = {
            "content": None,
            "embeds": None,
            "components": None
        }

        if embeds:
            embeds_json = []

            for i in embeds:
                embeds_json.append(_EmbedGenerator(i))

            _payload["embeds"] = embeds_json
        else:
            del _payload["embeds"]

        if content:
            _payload["content"] = content
        else:
            del _payload["content"]

        if action_row:
            if action_row.json["components"]:
                _payload["components"] = action_row.json
            else:
                del _payload["components"]

        if _payload:
            d = await _SendingRestHandler.execute(self.id, _payload, self._t)

            return DisMessage(d, self._t)
        else:
            return None

    async def send(self, content: Optional[str] = None, embed: Optional[DisEmbed] = None, action_row: Optional[ActionRow] = None) -> DisMessage:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embed: DisEmbed = None -> Embed for message (DisEmbed - embed) (default is None)
        :param action_row: ActionRow = None -> Action Row with components (default is None)
        :return DisMessage: Message which was sended
        """
        _payload = {
            "content": None,
            "embeds": None,
            "components": None
        }

        if embed:
            _payload["embeds"] = [_EmbedGenerator(embed)]
        else:
            del _payload["embeds"]

        if content:
            _payload["content"] = content
        else:
            del _payload["content"]

        if action_row:
            if action_row.json["components"]:
                _payload["components"] = action_row.json
            else:
                del _payload["components"]

        if _payload:
            d = await _SendingRestHandler.execute(self.id, _payload, self._t)

            return DisMessage(d, self._t)
        else:
            return None

    def fetch(self, id: int) -> DisMessage:
        """
        Fetch message
        -----
        :param id: Id of message
        :return DisMessage:
        """
        d = _GettingChannelData.fetch(self.id, self._t, id)

        return DisMessage(d, self._t)

    async def delete(self):
        _u = f"https://discord.com/api/v10/channels/{self.id}"

        await _SendingRestHandler.delete_channel(_u, self._t)


class DisDmChannel:
    """
    The class for sending messages to discord DMchannels and fetching messages in DMchannels
    """
    def __init__(self, dm_id: dict, token):
        """
        Init object
        -----
        :param id: Id of channel
        :param api: DisApi object with token
        """
        _data = _GettingChannelData.execute(dm_id, token)

        self.id = _data["id"]
        self._t = token

    async def send(self, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None, action_row: Optional[ActionRow] = None) -> Union[DisMessage, None]:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embeds: list[DisEmbed] = None -> Embeds for message (DisEmbed - embed) (default is None)
        :param action_row: ActionRow = None -> Action Row with components (default is None)
        :return DisMessage: Message which was sended
        """
        _payload = {
            "content": None,
            "embeds": None,
            "components": None
        }

        if embeds:
            embeds_json = []

            for i in embeds:
                embeds_json.append(_EmbedGenerator(i))

            _payload["embeds"] = embeds_json
        else:
            del _payload["embeds"]

        if content:
            _payload["content"] = content
        else:
            del _payload["content"]

        if action_row:
            if action_row.json["components"]:
                _payload["components"] = action_row.json
            else:
                del _payload["components"]

        if _payload:
            d = await _SendingRestHandler.execute(self.id, _payload, self._t)

            return DisMessage(d, self._t)
        else:
            return None

    async def send(self, content: Optional[str] = None, embed: Optional[DisEmbed] = None, action_row: Optional[ActionRow] = None) -> DisMessage:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embed: DisEmbed = None -> Embed for message (DisEmbed - embed) (default is None)
        :param action_row: ActionRow = None -> Action Row with components (default is None)
        :return DisMessage: Message which was sended
        """
        _payload = {
            "content": None,
            "embeds": None,
            "components": None
        }

        if embed:
            _payload["embeds"] = [_EmbedGenerator(embed)]
        else:
            del _payload["embeds"]

        if content:
            _payload["content"] = content
        else:
            del _payload["content"]

        if action_row:
            if action_row.json["components"]:
                _payload["components"] = action_row.json
            else:
                del _payload["components"]

        if _payload:
            d = await _SendingRestHandler.execute(self.id, _payload, self._t)

            return DisMessage(d, self._t)
        else:
            return None
