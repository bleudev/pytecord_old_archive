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
    Any
)

__all__: tuple[str] = (
    "ApplicationCommandType",
    "ApplicationCommand",
    "Option",
    "OptionType",
    "SlashCommand",
    "UserCommand",
    "MessageCommand",
    "Context",
    "Args"
)


class _MessageFlags:
    """
    Flags for messages in discord API. Varibles is constants.

    This use in send() method of Context class.
    """
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8


class ApplicationCommandType:
    """
    Application command types (see discord docs)
    """
    TEXT_INPUT = 1  # Slash Command
    USER = 2  # User Command
    MESSAGE = 3  # Message Command


class ApplicationCommand:
    """
    Application Command object.

    This use as parent for slash commands, message commands, user commands

    :var name: Name of application command
    :var cmd: Method to use in on_interaction
    :var command_type: Type of application command
    """
    def __init__(self, name, cmd, command_type: int):
        self.name = name
        self.cmd = cmd
        self.command_type = command_type


class Option:
    """
    Class for using options in application commands (TEXT_INPUT)
    """
    def __init__(self, name, description, option_type: int, choices: Optional[list[dict]] = None, required: bool = False):
        """
        Init class
        -----
        :param name: Name of option
        :param description: Description of option
        :param option_type: Type of option
        :param choices: Option's Choices
        :param required: Option's required var (bool)
        """
        self.name = name
        self.description = description
        self.option_type = option_type
        self.choices = choices
        self.required = required

    def json(self) -> dict:
        """
        Get json data of option
        -----
        :return dict: Json data of option
        """
        if self.option_type == OptionType.STRING or self.option_type == OptionType.INTEGER or self.option_type == OptionType.NUMBER and self.choices:
            if self.choices:
                return {
                    "name": self.name,
                    "description": self.description,
                    "type": self.option_type,
                    "choices": self.choices,
                    "required": self.required
                }
            else:
                return {
                    "name": self.name,
                    "description": self.description,
                    "type": self.option_type,
                    "required": self.required
                }
        else:
            return {
                "name": self.name,
                "description": self.description,
                "type": self.option_type,
                "required": self.required
            }


class OptionType:
    """
    Option types (see discord docs)
    """
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class SlashCommand(ApplicationCommand):
    def __init__(self, name, description, cmd, options: list[Option] = None):
        super().__init__(name, cmd, 1)

        self.description = description

        if not options:
            _options_jsons = []

            for o in options:
                _options_jsons.append(o.json())

            self.options = _options_jsons
        else:
            self.options = None


class UserCommand(ApplicationCommand):
    def __init__(self, name, cmd):
        super().__init__(name, cmd, 2)


class MessageCommand(ApplicationCommand):
    def __init__(self, name, cmd):
        super().__init__(name, cmd, 3)


class Context:
    """
    Class for receiving interaction content and sending messages to users

    There are some methods for responding to interaction (Slash Command)
    """
    def __init__(self, interaction_token, interaction_id, bot_token):
        self._interaction_token = interaction_token
        self._interaction_id = interaction_id
        self._headers = {'Authorization': f'Bot {bot_token}'}

    async def send(self, content: str, ephemeral: bool = False) -> None:
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




class _Argument:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value


class Args:
    def __init__(self, values=None):
        if values is None:
            values = []
        self._v: list[_Argument] = values

    def isempty(self) -> bool:
        return len(self._v) == 0

    def get(self, name: str) -> Any:
        for a in self._v:
            if a.name == name:
                return a.value

    def getString(self, name: str) -> str:
        for a in self._v:
            if a.name == name and a.type == OptionType.STRING:
                return str(a.value)

    def getInteger(self, name: str) -> int:
        for a in self._v:
            if a.name == name and a.type == OptionType.INTEGER:
                return int(a.value)

    def getNumber(self, name: str) -> int:
        for a in self._v:
            if a.name == name and a.type == OptionType.NUMBER:
                return int(a.value)

    def getBoolean(self, name: str) -> bool:
        for a in self._v:
            if a.name == name and a.type == OptionType.BOOLEAN:
                return bool(a.value)
