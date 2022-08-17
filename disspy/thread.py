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

__all__: tuple = (
    "DisNewsThread",
    "DisThread",
    "DisPrivateThread"
)

from aiohttp import ClientSession
from json import dumps


class DisNewsThread:
    def __init__(self, data, token) -> None:
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._t = token

    async def send(self, content: str):
        _u = f"https://discord.com/api/v10/channels/{self.id}/messages"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        _payload = {
            "content": content
        }

        async with ClientSession(headers=_hdrs) as session:
            await session.post(_u, data=dumps(_payload))


class DisThread:
    def __init__(self, data, token) -> None:
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._t = token
    
    async def send(self, content: str):
        _u = f"https://discord.com/api/v10/channels/{self.id}/messages"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        _payload = {
            "content": content
        }

        async with ClientSession(headers=_hdrs) as session:
            await session.post(_u, data=dumps(_payload))


class DisPrivateThread:
    def __init__(self, data, token) -> None:
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._t = token

    async def send(self, content: str):
        _u = f"https://discord.com/api/v10/channels/{self.id}/messages"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        _payload = {
            "content": content
        }

        async with ClientSession(headers=_hdrs) as session:
            await session.post(_u, data=dumps(_payload))
