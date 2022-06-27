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

from typing import (
    Optional,
    TypeVar
)


__all__: tuple[str] = (
    "DisEmoji",
    "DisReaction"
)


class DisEmoji:
    _T = TypeVar("DisEmoji")

    @property
    def __class__(self) -> TypeVar:
        return self._T

    def __init__(self, unicode: str):
        self.unicode = unicode


class DisReaction:
    _T = TypeVar("DisReaction")

    @property
    def __class__(self) -> TypeVar:
        return self._T

    def __init__(self, emoji: str, message_id, channel_id, token):
        self.emoji = emoji
        self._u = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        self._t = token

    async def delete(self):
        from aiohttp import ClientSession

        async with ClientSession(headers={'Authorization': f'Bot {self._t}', 'content-type': 'application/json'}) as s:
            await s.delete(self._u)
