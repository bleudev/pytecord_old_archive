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

from typing import Optional
from aiohttp import ClientSession

from disspy.user import User

__all__: tuple = ("DisEmoji", "DisOwnReaction", "DisReaction", "DisRemovedReaction")


class DisEmoji:
    """
    Emoji for reaction and other things
    """

    def __init__(
        self,
        unicode: Optional[str] = None,
        name: Optional[str] = None,
        emoji_id: Optional[int] = None,
    ) -> None:
        self.unicode = unicode
        self.name = name
        self.emoji_id = emoji_id

        if name is not None:
            if emoji_id is not None:
                self.type = "custom"
            else:
                self.type = "normal"
        else:
            self.type = "normal"


class DisOwnReaction:
    """
    Bot's own reaction
    """

    def __init__(
        self, emoji: str, message_id, channel_id, token, session: ClientSession
    ):
        self.emoji = emoji
        _mainurl = "https://discord.com/api/v10/"
        self._u = f"{_mainurl}channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        self._t = token

        self._session = session

    async def delete(self):
        """delete()

        Delete own reaction
        """
        await self._session.delete(self._u)


class DisReaction:
    """
    Reaction
    """

    def __init__(
        self,
        user: User,
        message_id: int,
        channel_id: int,
        guild_id: int,
        emoji: DisEmoji,
        token: str,
    ) -> None:
        self.user = user
        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.emoji = emoji
        self._t = token


class DisRemovedReaction:
    """
    Removed reaction
    """

    def __init__(
        self,
        message_id: int,
        channel_id: int,
        guild_id: int,
        emoji: DisEmoji,
        token: str,
    ) -> None:
        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.emoji = emoji
        self._t = token
