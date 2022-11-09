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

__all__: tuple = ("Emoji", "Reaction")


class Emoji:
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


class Reaction:
    """
    Any reaction
    """
    def __init__(self, __data: dict, __token: str, __session: ClientSession) -> None:
        self._t = __token
        self._s = __session

        _mainurl = "https://discord.com/api/v10/"
        _c_id = __data['channel_id']
        _m_id = __data['message_id']
        _e = __data['emoji']
        self._u = f"{_mainurl}channels/{_c_id}/messages/{_m_id}/reactions/{_e}/@me"

        def _try(k: str):
            try:
                return __data[k]
            except KeyError:
                return None

        self.user: User = _try('user')
        self.channel_id: int = __data['channel_id']
        self.message_id: int = __data['message_id']
        self.guild_id: int = __data['guild_id']
        self.emoji: Emoji = __data['emoji']

    async def delete(self) -> None:
        """
        Delete reaction
        """
        await self._s.delete(self._u)
