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
    final,
    overload
)

from disspy.embed import DisEmbed
from disspy.jsongenerators import _EmbedGenerator


@final
class DisMessage:
    def __init__(self, _data, _token):
        from disspy.channel import DisChannel

        self.channel = DisChannel(_data["channel_id"], _token)

        self._headers = {'Authorization': f'Bot {_token}', "content-type": "application/json"}

        self.content = _data["content"]
        self.id = _data["id"]

        self._t = _token

    @overload
    async def reply(self, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        _url = ""

        _d = {}

        if embeds:
            embeds_json = []

            for i in embeds:
                embeds_json.append(_EmbedGenerator(i))
            if content:
                _d = {
                    "content": content,
                    "embeds": embeds_json
                }
            elif not content:
                _d = {
                    "embeds": embeds_json
                }
        elif not embeds and content:
            _d = {
                "content": content
            }
        elif not embeds and not content:
            return

        from aiohttp import ClientSession

        async with ClientSession(headers=self._headers) as s:
            async with s.post(_url, data=_d) as p:
                d = await p.json()

                return DisMessage(d, self._t)

    @overload
    async def reply(self, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        _url = ""

        _payload = {}

        if embed and content:
            _payload = {
                "content": content,
                "embeds": [_EmbedGenerator(embed)]
            }
        elif embed and not content:
            _payload = {
                "embeds": [_EmbedGenerator(embed)]
            }

        elif content and not embed:
            _payload = {
                "content": content
            }
        elif not content and not embed:
            return

        from aiohttp import ClientSession

        async with ClientSession(headers=self._headers) as s:
            async with s.post(_url, data=_payload) as p:
                d = await p.json()

                return DisMessage(d, self._t)

