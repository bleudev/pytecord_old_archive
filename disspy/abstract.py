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
    List,
    Any,
    ClassVar,
    final
)

from abc import ABC, abstractmethod
from enum import Enum, auto, unique

__all__: tuple = (
    "Channel",
    "Thread",
    "Message"
)


class _AutoValue(Enum):
    def _generate_next_value_(name, start, count, last_values):
        if count > 12:
            return count + 1

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


class Channel(ABC):
    """Channel
    Any channel in discord

    (Abstract class)
    """
    @abstractmethod
    async def send(self, content: Optional[str] = None, embeds: Optional[List[Any]] = None,
                   action_row: Optional[Any] = None) -> Any:
        """send
        Send message in channel

        Args:
            content (Optional[str], optional): Message content. Defaults to None.
            embeds (Optional[List[Any]], optional): Message embeds. Defaults to None.
            action_row (Optional[Any], optional): Action row with components. Defaults to None.

        Returns:
            Any
        """
        return


class Thread(ABC):
    """Thread
    Any thread in discord

    (Abstract class)
    """
    def __init__(self) -> None:
        return

class Message(ABC):
    """Message
    Any message in discord

    (Abstract class)
    """
    def __init__(self, message_type: int, is_dm: bool = False) -> None:
        super().__init__()

        self._type = message_type
        self._is_dm = is_dm

    @abstractmethod
    async def reply(self, content: Optional[str] = None, embeds: Optional[List[Any]] = None):
        """reply
        Reply to message

        Args:
            content (Optional[str], optional): Message content. Defaults to None.
            embeds (Optional[List[Any]], optional): Message embeds. Defaults to None.
        """
        return

    def is_reply(self) -> bool:
        """is_reply
        Message is reply?

        Returns:
            bool: Message is reply?
        """
        return self._type == _MessageType.REPLY.value

    def is_default(self) -> bool:
        """is_default
        Message is default?

        Returns:
            bool: Message is default?
        """
        return self._type == _MessageType.DEFAULT.value

    def is_normal(self) -> bool:
        """is_normal
        Message channel is normal?

        Returns:
            bool: Is normal?
        """
        return self._is_dm is False

    def is_direct(self) -> bool:
        """is_direct
        Message channel is direct?

        Returns:
            bool: Is direct?
        """
        return self._is_dm
