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
    Any,
    List
)

from enum import Enum, unique, auto
from json import dumps
from aiohttp import ClientSession

from disspy.embed import DisEmbed
from disspy.jsongenerators import _EmbedGenerator
from disspy.reaction import DisEmoji, DisOwnReaction


class _AutoValue(Enum):
    def _generate_next_value_(name, start, count, last_values):
        if count > 12:
            return count + 1
        else:
            return count

@final
@unique
class _MessageType(_AutoValue):
    DEFAULT: ClassVar[int] = auto()
    RECIPIENT_ADD: ClassVar[int] = auto()
    RECIPIENT_REMOVE: ClassVar[int] = auto()
    CALL: ClassVar[int] = auto()
    CHANNEL_NAME_CHANGE: ClassVar[int] = auto()
    CHANNEL_ICON_CHANGE: ClassVar[int] = auto()
    CHANNEL_PINNED_MESSAGE: ClassVar[int] = auto()
    GUILD_MEMBER_JOIN: ClassVar[int] = auto()
    USER_PREMIUM_GUILD_SUBSCRIPTION: ClassVar[int] = auto()
    GUILD_BOOST_TIER_1: ClassVar[int] = auto()
    GUILD_BOOST_TIER_2: ClassVar[int] = auto()
    GUILD_BOOST_TIER_3: ClassVar[int] = auto()
    CHANNEL_FOLLOW_ADD: ClassVar[int] = auto()
    GUILD_DISCOVERY_DISQUALIFIED: ClassVar[int] = auto()
    GUILD_DISCOVERY_REQUALIFIED: ClassVar[int] = auto()
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING: ClassVar[int] = auto()
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING: ClassVar[int] = auto()
    THREAD_CREATED: ClassVar[int] = auto()
    REPLY: ClassVar[int] = auto()
    CHAT_INPUT_COMMAND: ClassVar[int] = auto()
    THREAD_STARTER_MESSAGE: ClassVar[int] = auto()
    GUILD_INVITE_REMINDER: ClassVar[int] = auto()
    CONTEXT_MENU_COMMAND: ClassVar[int] = auto()
    AUTO_MODERATION_ACTION: ClassVar[int] = auto()


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
        _u = f"https://discord.com/api/v10/channels/{channel_id}/messages"

        async with ClientSession(headers=hdrs) as session:
            async with session.post(_u, data=dump_data) as post_data:
                j = await post_data.json()

                return j

    @staticmethod
    async def create_reaction(endpoint, token):
        """create_reaction()

        Args:
            endpoint (str): Url endpoint
            token (str): Bot token
        """
        async with ClientSession(headers={'Authorization': f'Bot {token}',
                                          'content-type': 'application/json'}) as session:
            _u = f"https://discord.com/api/v10{endpoint}"

            await session.put(_u)

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

    async def reply(self, content: Optional[Any] = None, embeds: Optional[List[DisEmbed]] = None):
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

    async def reply(self, content: Optional[Any] = None, embeds: Optional[List[DisEmbed]] = None):
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
