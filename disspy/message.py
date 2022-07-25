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
    "DisMessage",
    "DmMessage",
    "MessageDeleteEvent",
    "DmMessageDeleteEvent"
)

from typing import (
    Optional,
    Union,
    final,
    ClassVar,
    Any
)
from json import dumps
from aiohttp import ClientSession

from disspy.embed import DisEmbed
from disspy.jsongenerators import _EmbedGenerator
from disspy.reaction import DisEmoji, DisOwnReaction


class _MessageType:
    DEFAULT: ClassVar[int] = 0
    RECIPIENT_ADD: ClassVar[int] = 1
    RECIPIENT_REMOVE: ClassVar[int] = 2
    CALL: ClassVar[int] = 3
    CHANNEL_NAME_CHANGE: ClassVar[int] = 4
    CHANNEL_ICON_CHANGE: ClassVar[int] = 5
    CHANNEL_PINNED_MESSAGE: ClassVar[int] = 6
    GUILD_MEMBER_JOIN: ClassVar[int] = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION: ClassVar[int] = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1: ClassVar[int] = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2: ClassVar[int] = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3: ClassVar[int] = 11
    CHANNEL_FOLLOW_ADD: ClassVar[int] = 12
    GUILD_DISCOVERY_DISQUALIFIED: ClassVar[int] = 14
    GUILD_DISCOVERY_REQUALIFIED: ClassVar[int] = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING: ClassVar[int] = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING: ClassVar[int] = 17
    THREAD_CREATED: ClassVar[int] = 18
    REPLY: ClassVar[int] = 19
    CHAT_INPUT_COMMAND: ClassVar[int] = 20
    THREAD_STARTER_MESSAGE: ClassVar[int] = 21
    GUILD_INVITE_REMINDER: ClassVar[int] = 22
    CONTEXT_MENU_COMMAND: ClassVar[int] = 23


@final
class _SendingRestHandler:
    @staticmethod
    async def execute(channel_id: int, payload: dict, token: str):
        """execute()

        Args:
            channel_id (int): Channel id
            payload (dict): Json payload
            token (str): Bot token

        Returns:
            dict: Json data
        """
        dump_data = dumps(payload)
        hdrs = {'Authorization': f'Bot {token}', 'content-type': 'application/json'}
        _u = f"https://discord.com/api/v9/channels/{channel_id}/messages"

        async with ClientSession(headers=hdrs) as session:
            async with session.post(_u, data=dump_data) as post_data:
                j = await post_data.json()

                return j

    @staticmethod
    async def create_reaction(endpoint, token):
        async with ClientSession(headers={'Authorization': f'Bot {token}', 'content-type': 'application/json'}) as s:
            _u = f"https://discord.com/api/v10{endpoint}"

            await s.put(_u)

    @staticmethod
    async def delete_message(url, token):
        async with ClientSession(headers={'Authorization': f'Bot {token}', 'content-type': 'application/json'}) as s:
            await s.delete(url=url)


@final
class DisMessage:
    def __init__(self, _data, _token):
        from disspy.channel import DisChannel

        self.json = _data

        self.channel = DisChannel(_data["channel_id"], _token)

        self.content: str = str(_data["content"])

        self.id: int = int(_data["id"])
        self._type: int = int(_data["type"])

        self._t = _token

    def is_reply(self) -> bool:
        return self._type == _MessageType.REPLY

    def is_default(self) -> bool:
        return self._type == _MessageType.DEFAULT

    async def reply(self, content: Optional[Any] = None, embeds: Optional[list[DisEmbed]] = None):
        _d = {
            "content": None,
            "embeds": {},
            "message_reference": {
                "message_id": self.id
            }
        }

        content = str(content)

        if content:
            _d["content"] = content

        if embeds:
            embeds_jsons = []

            for i in embeds:
                embeds_jsons.append(_EmbedGenerator(i))

            _d["embeds"] = embeds_jsons

        if not embeds and not content:
            return

        await _SendingRestHandler.execute(self.channel.id, _d, self._t)

    async def create_reaction(self, emoji: Union[DisEmoji, str]) -> DisOwnReaction:
        if isinstance(emoji, DisEmoji):
            if emoji.type == "custom":
                emoji = f"{emoji.name}:{str(emoji.emoji_id)}"
            elif emoji.type == "normal":
                emoji = emoji.unicode

        await _SendingRestHandler.create_reaction(f"/channels/{self.channel.id}/messages/{self.id}/reactions/{emoji}/@me", self._t)

        return DisOwnReaction(emoji, self.id, self.channel.id, self._t)

    async def delete(self):
        _u = f"https://discord.com/api/v10/channels/{self.channel.id}/messages/{self.id}"

        await _SendingRestHandler.delete_message(_u, self._t)


class DmMessage:
    def __init__(self, d, token):
        from disspy.channel import DisDmChannel

        self.json = d
        self._t = token

        self.id = d["id"]

        self.content = d["content"]
        self.channel = DisDmChannel(d["channel_id"], self._t)

        self._type: int = int(d["type"])

    def is_reply(self) -> bool:
        return self._type == _MessageType.REPLY

    def is_default(self) -> bool:
        return self._type == _MessageType.DEFAULT

    async def reply(self, content: Optional[Any] = None, embeds: Optional[list[DisEmbed]] = None):
        _d = {
            "content": None,
            "embeds": {},
            "message_reference": {
                "message_id": self.id
            }
        }

        content = str(content)

        if content:
            _d["content"] = content

        if embeds:
            embeds_jsons = []

            for i in embeds:
                embeds_jsons.append(_EmbedGenerator(i))

            _d["embeds"] = embeds_jsons

        if not embeds and not content:
            return

        await _SendingRestHandler.execute(self.channel.id, _d, self._t)

    async def create_reaction(self, emoji: Union[DisEmoji, str]) -> DisOwnReaction:
        if isinstance(emoji, DisEmoji):
            if emoji.type == "custom":
                emoji = f"{emoji.name}:{str(emoji.emoji_id)}"
            elif emoji.type == "normal":
                emoji = emoji.unicode

        await _SendingRestHandler.create_reaction(f"/channels/{self.channel.id}/messages/{self.id}/reactions/{emoji}/@me", self._t)

        return DisOwnReaction(emoji, self.id, self.channel.id, self._t)


class MessageDeleteEvent:
    def __init__(self, d: dict, t: str):
        from disspy.channel import DisChannel

        self.message_id = d['id']
        self.channel = DisChannel(d['channel_id'], t)


class DmMessageDeleteEvent:
    def __init__(self, d: dict, t: str):
        from disspy.channel import DisDmChannel

        self.message_id = d['id']
        self.channel = DisDmChannel(d['channel_id'], t)
