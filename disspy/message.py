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

__all__: tuple[str] = (
    "DisMessage"
)

from typing import (
    Optional,
    final
)

from disspy.embed import DisEmbed
from disspy.jsongenerators import _EmbedGenerator


class _SendingRestHandler:
    @staticmethod
    async def execute(channel_id, payload, token):
        from aiohttp import ClientSession as CS

        async with CS(headers={'Authorization': f'Bot {token}'}) as s:
            _u = f"https://discord.com/api/v9/channels/{channel_id}/messages"

            async with s.post(_u, data=payload) as p:
                j = await p.json()

                return j


@final
class DisMessage:
    def __init__(self, _data, _token):
        from disspy.channel import DisChannel

        self.channel = DisChannel(_data["channel_id"], _token)

        self._headers = {'Authorization': f'Bot {_token}'}

        self.content = _data["content"]
        self.id = _data["id"]

        self._t = _token

    async def reply(self, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        _url = f"https://discord.com/api/v9/channels/{self.channel.id}/messages"

        _d = {}

        if embeds:
            embeds_json = []

            for i in embeds:
                embeds_json.append(_EmbedGenerator(i))
            if content:
                _d = {
                    "content": content,
                    "embeds": embeds_json,
                    "message_reference": {
                        "message_id": self.id,
                        "guild_id": self.channel.guild_id
                    }
                }
            elif not content:
                _d = {
                    "embeds": embeds_json,
                    "message_reference": {
                        "message_id": self.id,
                        "guild_id": self.channel.guild_id
                    }
                }
        elif not embeds and content:
            _d = {
                "content": content,
                "message_reference": {
                    "message_id": self.id,
                    "guild_id": self.channel.guild_id
                }
            }
        elif not embeds and not content:
            return

        d = await _SendingRestHandler.execute(self.channel.id, _d, self._t)

        print(d)

    async def reply(self, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        _url = f"https://discord.com/api/v9/channels/{self.channel.id}/messages"

        _payload = {}

        if embed and content:
            _payload = {
                "content": content,
                "embeds": [_EmbedGenerator(embed)],
                "message_reference": {
                    "message_id": self.id,
                    "guild_id": self.channel.guild_id
                }
            }
        elif embed and not content:
            _payload = {
                "embeds": [_EmbedGenerator(embed)],
                "message_reference": {
                    "message_id": self.id,
                    "guild_id": self.channel.guild_id
                }
            }

        elif content and not embed:
            _payload = {
                "content": content,
                "message_reference": {
                    "message_id": self.id,
                    "guild_id": self.channel.guild_id
                }
            }
        elif not content and not embed:
            return

        d = await _SendingRestHandler.execute(self.channel.id, _payload, self._t)

        print(d)
