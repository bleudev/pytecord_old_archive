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
    Union,
    final,
    ClassVar
)

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
    async def execute(channel_id, payload, token):
        from aiohttp import ClientSession
        from json import dumps

        ds = dumps(payload)

        async with ClientSession(headers={'Authorization': f'Bot {token}', 'content-type': 'application/json'}) as s:
            _u = f"https://discord.com/api/v9/channels/{channel_id}/messages"

            async with s.post(_u, data=ds) as p:
                j = await p.json()

                return j

    @staticmethod
    async def create_reaction(endpoint, token):
        from aiohttp import ClientSession

        async with ClientSession(headers={'Authorization': f'Bot {token}', 'content-type': 'application/json'}) as s:
            _u = f"https://discord.com/api/v10{endpoint}"
            print(_u)
            await s.put(_u)


@final
class DisMessage:
    def __init__(self, _data, _token):
        from disspy.channel import DisChannel

        self._json = _data

        self.channel: DisChannel = DisChannel(_data["channel_id"], _token)

        self._headers = {'Authorization': f'Bot {_token}'}

        self.content: str = str(_data["content"])

        self.id: int = int(_data["id"])
        self._type: int = int(_data["type"])

        self._t = _token

    def is_reply(self) -> bool:
        return self._type == _MessageType.REPLY

    def is_default(self) -> bool:
        return self._type == _MessageType.DEFAULT

    async def reply(self, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        _d = {
            "content": None,
            "embeds": {},
            "message_reference": {
                "message_id": self.id
            }
        }

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

    async def reply(self, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        _d = {
            "content": None,
            "embeds": {},
            "message_reference": {
                "message_id": self.id
            }
        }

        if embed:
            _d["embeds"] = [_EmbedGenerator(embed)]

        if content:
            _d["content"] = content

        if not content and not embed:
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
    def __init__(self, d: dict):
        self.message_id = d['id']
        self.channel_id = d['channel_id']
        self.guild_id = d['guild_id']
