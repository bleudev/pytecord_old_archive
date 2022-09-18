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
from typing import (
    Optional,
    List,
    Any,
    Union
)
from json import dumps
from aiohttp import ClientSession


from disspy.abstract import Thread
from disspy.jsongenerators import _EmbedGenerator
from disspy.channel import DisMessage
from disspy.ui import ActionRow
from disspy.typ import (
    SupportsStr,
    MISSING
)


class _Thread:
    def __init__(self, __id, __session, __token) -> None:
        self._id = __id
        self.session = __session
        self._t = __token

    async def send_message(self, content: Optional[SupportsStr] = MISSING,
                            embeds: Optional[List[Any]] = MISSING,
                            action_row: Optional[ActionRow] = MISSING):
        """send_message
        Send message to thread
        """
        _u = f"https://discord.com/api/v10/channels/{self._id}/messages"

        _payload = {
            "content": None,
            "embeds": None,
            "components": None
        }

        if content:
            content = str(content)

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
            async with self.session.post(_u, data=dumps(_payload)) as post_message:
                data = await post_message.json()

                return DisMessage(data, self._t, self.session)

        return None

    async def delete(self):
        """delete
        Delete thread
        """
        _u = f"https://discord.com/api/v10/channels/{self._id}"
        await self.session.delete(_u)


class DisNewsThread(Thread):
    """
    Channel with GUILD_NEWS_THREAD type
    """
    def __init__(self, data, token, __session: ClientSession) -> None:
        super().__init__()
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._thread_client = _Thread(self.id, __session, token)

    async def send(self, content: Optional[SupportsStr] = MISSING,
                   embeds: Optional[List[Any]] = MISSING,
                   action_row: Optional[ActionRow] = MISSING) -> Union[DisMessage, None]:
        """send
        Send message in thread

        Args:
            content (SupportsStr, optional): Message content. Defaults to MISSING.
            embeds (List[Any], optional): Message embeds. Defaults to MISSING.
            action_row (ActionRow, optional): Action row with components. Defaults to MISSING.

        Returns:
            DisMessage: Sended message
            None
        """
        return await self._thread_client.send_message(content, embeds, action_row)

    async def delete(self):
        """delete
        Delete thread
        """
        await self._thread_client.delete()


class DisThread(Thread):
    """
    Channel with GUILD_PUBLIC_THREAD type
    """
    def __init__(self, data, token, __session: ClientSession) -> None:
        super().__init__()
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._thread_client = _Thread(self.id, __session, token)

    async def send(self, content: Optional[SupportsStr] = MISSING,
                   embeds: Optional[List[Any]] = MISSING,
                   action_row: Optional[ActionRow] = MISSING) -> Union[DisMessage, None]:
        """send
        Send message in thread

        Args:
            content (SupportsStr, optional): Message content. Defaults to MISSING.
            embeds (List[Any], optional): Message embeds. Defaults to MISSING.
            action_row (ActionRow, optional): Action row with components. Defaults to MISSING.

        Returns:
            DisMessage: Sended message
            None
        """
        return await self._thread_client.send_message(content, embeds, action_row)

    async def delete(self):
        """delete
        Delete thread
        """
        await self._thread_client.delete()


class DisPrivateThread(Thread):
    """
    Channel with GUILD_PRIVATE_THREAD type
    """
    def __init__(self, data, token, __session: ClientSession) -> None:
        super().__init__()
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.parent_id: int = int(data["parent_id"])
        self.owner_id: int = int(data["owner_id"])

        self.archived: bool = data["thread_metadata"]["archived"]

        self.name: str = data["name"]

        self._thread_client = _Thread(self.id, __session, token)

    async def send(self, content: Optional[SupportsStr] = MISSING,
                   embeds: Optional[List[Any]] = MISSING,
                   action_row: Optional[ActionRow] = MISSING) -> Union[DisMessage, None]:
        """send
        Send message in thread

        Args:
            content (SupportsStr, optional): Message content. Defaults to MISSING.
            embeds (List[Any], optional): Message embeds. Defaults to MISSING.
            action_row (ActionRow, optional): Action row with components. Defaults to MISSING.

        Returns:
            DisMessage: Sended message
            None
        """
        return await self._thread_client.send_message(content, embeds, action_row)

    async def delete(self):
        """delete
        Delete thread
        """
        await self._thread_client.delete()
