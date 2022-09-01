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

from json import dumps
from aiohttp import ClientSession
from abstract import Thread


class DisNewsThread(Thread):
    """
    Channel with GUILD_NEWS_THREAD type
    """
    def __init__(self, data, token) -> None:
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._t = token

    async def send(self, content: str):
        """send
        Send message in thread

        Args:
            content (str): Message content
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/messages"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        _payload = {
            "content": content
        }

        async with ClientSession(headers=_hdrs) as session:
            await session.post(_u, data=dumps(_payload))

    async def delete(self):
        """delete
        Delete thread
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        async with ClientSession(headers=_hdrs) as session:
            await session.delete(_u)


class DisThread(Thread):
    """
    Channel with GUILD_PUBLIC_THREAD type
    """
    def __init__(self, data, token) -> None:
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._t = token

    async def send(self, content: str):
        """send
        Send message in thread

        Args:
            content (str): Message content
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/messages"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        _payload = {
            "content": content
        }

        async with ClientSession(headers=_hdrs) as session:
            await session.post(_u, data=dumps(_payload))

    async def delete(self):
        """delete
        Delete thread
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        async with ClientSession(headers=_hdrs) as session:
            await session.delete(_u)


class DisPrivateThread(Thread):
    """
    Channel with GUILD_PRIVATE_THREAD type
    """
    def __init__(self, data, token) -> None:
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._t = token

    async def send(self, content: str):
        """send
        Send message in thread

        Args:
            content (str): Message content
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/messages"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        _payload = {
            "content": content
        }

        async with ClientSession(headers=_hdrs) as session:
            await session.post(_u, data=dumps(_payload))

    async def delete(self):
        """delete
        Delete thread
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}"
        _hdrs = {'Authorization': f'Bot {self._t}',
                 'content-type': 'application/json'}

        async with ClientSession(headers=_hdrs) as session:
            await session.delete(_u)
