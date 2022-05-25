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

from typing import (
    Optional
)


class _SendingRestHandler:
    @staticmethod
    async def execute(id, payload, token):
        from aiohttp import ClientSession as CS

        async with CS(headers={'Authorization': f'Bot {token}'}) as s:
            _u = f"https://discord.com/api/v9/channels/{id}/messages"

            async with s.post(_u, data=payload) as p:
                j = await p.json()

                return j


class _GettingChannelData:
    @staticmethod
    def execute(id, token):
        from requests import get

        _u = f"https://discord.com/api/v9/channels/{id}"
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
            self.guild_id = _data["guild_id"]
        except KeyError:
            pass

    def __eq__(self, other):
        """
        __eq__ have using in "==" operator

        :param other: Other object (DisChannel)
        :return: bool -> if id of this object equals with id of other object :returns: True, else False:
        """
        return self.id == other.id

    async def send(self, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None) -> int:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embeds: list[DisEmbed] = None -> Embeds for message (DisEmbed - embed) (default is None)
        :return: None
        """
        _payload = {}
        if embeds:
            embeds_json = []

            for i in embeds:
                embeds_json.append(i.tojson())
            if content:
                _payload = {
                    "content": content,
                    "embeds": embeds_json
                }
            elif not content:
                _payload = {
                    "embeds": embeds_json
                }
        elif not embeds and content:
            _payload = {
                "content": content
            }
        elif not embeds and not content:
            return

        await _SendingRestHandler.execute(self.id, _payload, self._t)

        return 0

    async def send(self, content: Optional[str] = None, embed: Optional[DisEmbed] = None) -> int:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embed: DisEmbed = None -> Embed for message (DisEmbed - embed) (default is None)
        :return: None
        """
        _payload = {}

        if embed and content:
            _payload = {
                "content": content,
                "embeds": [embed.tojson()]
            }
        elif embed and not content:
            _payload = {
                "embeds": [embed.tojson()]
            }

        elif content and not embed:
            _payload = {
                "content": content
            }
        elif not content and not embed:
            return

        await _SendingRestHandler.execute(self.id, _payload, self._t)

        return 0

    def fetch(self, id: int):
        return DisMessage(id, self.id, self._a)


class DisDm:
    """
    The class for sending messages to discord DMchannels and fetching messages in DMchannels
    """
    def __init__(self, id, api):
        self._api = api
        self.id = id

    def fetch(self, id: int):
        return self._api.fetch(self.id, id)
