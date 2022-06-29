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
    Union,
    Optional,
    Any,
    NoReturn,
    ClassVar,
    Callable,
    final
)

from disspy.jsongenerators import _OptionGenerator
from disspy.core import Showflake

__all__: tuple[str] = (
    "ApplicationCommandType",
    "ApplicationCommand",
    "Option",
    "OptionType",
    "SlashCommand",
    "UserCommand",
    "MessageCommand",
    "Context",
    "OptionArgs"
)


@final
class _MessageFlags:
    """
    Flags for messages in discord API. Varibles is constants.

    This use in send() method of Context class.
    """
    CROSSPOSTED: ClassVar[int] = 1 << 0
    IS_CROSSPOST: ClassVar[int] = 1 << 1
    SUPPRESS_EMBEDS: ClassVar[int] = 1 << 2
    SOURCE_MESSAGE_DELETED: ClassVar[int] = 1 << 3
    URGENT: ClassVar[int] = 1 << 4
    HAS_THREAD: ClassVar[int] = 1 << 5
    EPHEMERAL: ClassVar[int] = 1 << 6
    LOADING: ClassVar[int] = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD: ClassVar[int] = 1 << 8


@final
class ApplicationCommandType:
    """
    Application command types (see discord docs)
    """
    TEXT_INPUT: ClassVar[int] = 1  # Slash Command
    USER: ClassVar[int] = 2  # User Command
    MESSAGE: ClassVar[int] = 3  # Message Command


class ApplicationCommand:
    """
    Application Command object.

    This use as parent for slash commands, message commands, user commands

    :var name: Name of application command
    :var cmd: Method to use in on_interaction
    :var command_type: Type of application command
    """
    def __init__(self, name: str, cmd: Callable, command_type: int) -> NoReturn:
        self.name: str = name
        self.cmd: Callable = cmd
        self.command_type: int = command_type


@final
class Option:
    """
    Class for using options in application commands (TEXT_INPUT)
    """
    def __init__(self, name: str, description: str, option_type: int, choices: Optional[list[dict]] = None, required: Optional[bool] = False) -> NoReturn:
        """
        Init class
        -----
        :param name: Name of option
        :param description: Description of option
        :param option_type: Type of option
        :param choices: Option's Choices
        :param required: Option's required var (bool)
        """
        self.name: str = name
        self.description: str = description
        self.option_type: int = option_type
        self.choices: Union[list[dict], None] = choices
        self.required: bool = required


@final
class OptionType:
    """
    Option types (see discord docs)
    """
    SUB_COMMAND: ClassVar[int] = 1
    SUB_COMMAND_GROUP: ClassVar[int] = 2
    STRING: ClassVar[int] = 3
    INTEGER: ClassVar[int] = 4
    BOOLEAN: ClassVar[int] = 5
    USER: ClassVar[int] = 6
    CHANNEL: ClassVar[int] = 7
    ROLE: ClassVar[int] = 8
    MENTIONABLE: ClassVar[int] = 9
    NUMBER: ClassVar[int] = 10
    ATTACHMENT: ClassVar[int] = 11


@final
class SlashCommand(ApplicationCommand):
    """
    Application Command with type number 1 (TEXT_INPUT)
    """
    def __init__(self, name: str, description: str, cmd: Callable, options: Optional[list[Option]] = None) -> NoReturn:
        super().__init__(name, cmd, 1)

        self.description = description

        if options:
            _options_jsons = []

            for o in options:
                _options_jsons.append(_OptionGenerator(o))

            self.options: Union[list[Option], None] = _options_jsons
        else:
            self.options: Union[list[Option], None] = None


@final
class UserCommand(ApplicationCommand):
    """
    Application Command with type number 2 (USER)
    """
    def __init__(self, name: str, cmd: Callable) -> NoReturn:
        super().__init__(name, cmd, 2)


@final
class MessageCommand(ApplicationCommand):
    """
    Application Command with type number 3 (MESSAGE)
    """
    def __init__(self, name: str, cmd: Callable) -> NoReturn:
        super().__init__(name, cmd, 3)


@final
class Context:
    """
    Class for receiving interaction content and sending messages to users

    There are some methods for responding to interaction (Slash Command)
    """
    def __init__(self, interaction_token: Union[Showflake[str], str], interaction_id: Union[Showflake[int], int], bot_token) -> NoReturn:
        self._interaction_token: str = str(interaction_token)
        self._interaction_id: int = int(interaction_id)
        self._headers = {'Authorization': f'Bot {bot_token}'}

    async def send(self, content: str, ephemeral: bool = False) -> NoReturn:
        """

        :param content: (str) Message content
        :param ephemeral: (bool) Sets message invisible for other member (not author)
        :return None:
        """
        _payload = {}

        if ephemeral:
            _payload = {
                "type": 4,
                "data": {
                    "content": content,
                    "flags": _MessageFlags.EPHEMERAL
                }
            }
        else:
            _payload = {
                "type": 4,
                "data": {
                    "content": content
                }
            }

        _url = f"https://discord.com/api/v9/interactions/{self._interaction_id}/{self._interaction_token}/callback"

        from requests import post

        post(_url, json=_payload, headers=self._headers)

        del post


@final
class _Argument:
    def __init__(self, name: str, type: int, value: Any) -> NoReturn:
        self.name: str = name
        self.type: int = type
        self.value: Any = value


@final
class OptionArgs:
    """
    Class for receiving option values in interactions

    Example
    @bot.slash_command("Test", "Wow", options=[Option("Hi", "lol", OptionType.STRING)])
    async def test(ctx: Context, args: OptionArgs):
        await ctx.send(args.getString("Hi"))
    """
    def __init__(self, values: Optional[list[_Argument]] = None) -> NoReturn:
        """
        Init object
        -----
        :param values: Option Values
        """
        if values is None:
            values = []
        self._v: list[_Argument] = values

    def isempty(self) -> bool:
        """
        Returns True or False when is empty is True or False
        -----
        :return bool: Is empty?
        """
        return len(self._v) == 0

    def get(self, name: str) -> Any:
        """
        Get value from name
        -----
        :param name: Name of option
        :return Any: Option value
        """
        for a in self._v:
            if a.name == name:
                return a.value

    def getString(self, name: str) -> str:
        """
        Get string value from name
        -----
        :param name: Name of option
        :return str: Option value (always string)
        """
        for a in self._v:
            if a.name == name and a.type == OptionType.STRING:
                return str(a.value)

    def getInteger(self, name: str) -> int:
        """
        Get integer value from na1me
        -----
        :param name: Name of option
        :return int: Option value (always integer)
        """
        for a in self._v:
            if a.name == name and a.type == OptionType.INTEGER:
                return int(a.value)

    def getNumber(self, name: str) -> int:
        """
        Get number value from name
        -----
        :param name: Name of option
        :return int: Option value (always integer)
        """
        for a in self._v:
            if a.name == name and a.type == OptionType.NUMBER:
                return int(a.value)

    def getBoolean(self, name: str) -> bool:
        """
        Get boolean value from name
        -----
        :param name: Name of option
        :return bool: Option value (always boolean)
        """
        for a in self._v:
            if a.name == name and a.type == OptionType.BOOLEAN:
                return bool(a.value)
