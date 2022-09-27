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

from typing import Union, Optional, Any, ClassVar, final, List, Tuple, Literal, Dict
from json import dumps
import aiohttp

from disspy.ui import ActionRow
from disspy.utils import dict_to_tuples

__all__: tuple = (
    "ApplicationCommandType",
    "Option",
    "StrOption",
    "IntOption",
    "NumOption",
    "BoolOption",
    "ChannelOption",
    "UserOption",
    "OptionType",
    "Context",
)


class Choice:
    """
    Class for using choices in options (STRING, INTEGER, NUMBER types only)
    """

    def __init__(self, name: str, value: Union[str, int, float]) -> None:
        self.name = value
        self.value = value


class Option:
    """
    Class for using options in application commands (TEXT_INPUT)
    """

    def __init__(self, type: int) -> None:
        """__init__
        Create option object

        Args:
            option_type (int): Option type

        Returns:
            None
        """
        self.option_description: str = "No description"
        self.option_type: int = type
        self.option_choices: Union[List[dict], None] = []
        self.is_required: bool = False

    def required(self):
        """required
        Set this option required

        Returns:
            Option: New option
        """
        option = Option(self.option_type)
        option.is_required = True
        option.option_choices = self.option_choices
        option.option_description = self.option_description

        return option

    def description(self, text: str):
        """set_description
        Set description to this option

        Args:
            text (str): Description

        Returns:
            Option: New option
        """
        option = Option(self.option_type)
        option.is_required = self.is_required
        option.option_choices = self.option_choices
        option.option_description = text

        return option

    def choices(self, choices: List[Choice]):
        """set_choices
        Set choices to this option

        Args:
            choices (List[dict]): Choices

        Returns:
            Option: New option
        """
        assert self.option_type in [
            3,
            4,
            10,
        ], "For using choices a your option must have STRING, INTEGER or NUMBER type!"

        option = Option(self.option_type)
        option.is_required = self.is_required
        option.option_description = self.option_description

        json_choices = []

        for i in choices:
            option_types = {3: str, 4: int, 10: float}
            option_type = option_types[self.option_type]

            assert isinstance(
                i.value, option_type
            ), "A your value type must be equal with a your option type!"
            json_choices.append({"name": i.name, "value": i.value})

        option.option_choices = json_choices

        return option


class _OptionsMethods:
    @staticmethod
    def describe(**options: Dict[str, Option]):
        """describe
        Describe options
        """

        def wrapper(func):
            result = []

            for name in list(options.keys()):
                value: Option = options[name]

                result.append(
                    {
                        "name": name,
                        "type": value.option_type,
                        "description": value.option_description,
                        "required": value.is_required,
                        "choices": value.option_choices,
                    }
                )
            try:
                to_edit = {"options": result}

                for key in list(func[0].keys()):
                    val = func[0][key]

                    to_edit.setdefault(key, val)

                return (to_edit, func[1])
            except TypeError:
                return ({"options": result}, func)

        return wrapper


class Localization:
    def __init__(self, *, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def json(self) -> dict:
        return {"name": self.name, "description": self.description}


options = _OptionsMethods()


def describe(description: str):
    """describe
    Desribe command

    Args:
        description (str): Description
    """

    def wrapper(func):
        try:
            to_edit = {"description": description}

            for key in list(func[0].keys()):
                val = func[0][key]

                to_edit.setdefault(key, val)

            return (to_edit, func[1])
        except TypeError:
            return ({"description": description}, func)

    return wrapper


def localize(**localizations: Dict[str, Localization]):
    parsed_info = {"name_localizations": {}, "description_localizations": {}}
    _localizations: list = dict_to_tuples(localizations)

    for lang, localization in _localizations:
        _json = localization.json()

        # Name
        _name = _json["name"]
        parsed_info["name_localizations"].setdefault(lang, _name)

        # Description
        _description = _json["description"]
        parsed_info["description_localizations"].setdefault(lang, _description)

    def wrapper(func):
        try:
            to_edit = parsed_info

            for key in list(func[0].keys()):
                val = func[0][key]

                to_edit.setdefault(key, val)

            return (to_edit, func[1])
        except TypeError:
            return (parsed_info, func)

    return wrapper


@final
class _MessageFlags:
    """
    Flags for messages in discord API. Variables are constants.

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


class _SendingRestHandler:
    @staticmethod
    async def execute(url, payload, token):
        """execute()

        Args:
            url (str): Url for post
            payload (_type_): Json payload for post
            token (_type_): Bot token for headers

        Returns:
            _type_: _description_
        """
        async with aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {token}",
                "content-type": "application/json",
            }
        ) as session:
            try:
                async with session.post(url, data=dumps(payload)) as data:
                    j = await data.json()

                    return j
            except aiohttp.ContentTypeError:
                await session.post(url, data=dumps(payload))


@final
class ApplicationCommandType:
    """
    Application command types (see discord docs)
    """

    TEXT_INPUT: ClassVar[int] = 1  # Slash Command
    USER: ClassVar[int] = 2  # User Command
    MESSAGE: ClassVar[int] = 3  # Message Command


@final
class OptionType:
    """
    Option types (see discord docs)
    """

    SUB_COMMAND: Literal[1] = 1
    SUB_COMMAND_GROUP: Literal[2] = 2
    STRING: Literal[3] = 3
    INTEGER: Literal[4] = 4
    BOOLEAN: Literal[5] = 5
    USER: Literal[6] = 6
    CHANNEL: Literal[7] = 7
    ROLE: Literal[8] = 8
    MENTIONABLE: Literal[9] = 9
    NUMBER: Literal[10] = 10
    ATTACHMENT: Literal[11] = 11


@final
class StrOption(Option):
    """StrOption
    Option with STRING type
    """

    def __init__(self) -> None:
        super().__init__(OptionType.STRING)


@final
class IntOption(Option):
    """StrOption
    Option with INTEGER type
    """

    def __init__(self) -> None:
        super().__init__(OptionType.INTEGER)


@final
class NumOption(Option):
    """StrOption
    Option with NUMBER type
    """

    def __init__(self) -> None:
        super().__init__(OptionType.NUMBER)


class BoolOption(Option):
    """StrOption
    Option with BOOLEAN type
    """

    def __init__(self) -> None:
        super().__init__(OptionType.BOOLEAN)


@final
class UserOption(Option):
    """StrOption
    Option with USER type
    """

    def __init__(self) -> None:
        super().__init__(OptionType.USER)


@final
class ChannelOption(Option):
    """StrOption
    Option with CHANNEL type
    """

    def __init__(self) -> None:
        super().__init__(OptionType.CHANNEL)


@final
class Context:
    """
    Class for receiving interaction content and sending messages to users

    There are some methods for responding to interaction (Slash Command)
    """

    def __init__(self, interaction_info: Tuple[str, int], bot_token) -> None:
        self._interaction_token: str = str(list(interaction_info)[0])
        self._interaction_id: int = int(list(interaction_info)[1])

        self._t = bot_token

    async def respond(
        self,
        *args,
        sep: Optional[str] = "\n",
        action_row: Optional[ActionRow] = None,
        ephemeral: bool = False,
    ) -> None:
        """

        :param content: (str) Message content
        :param ephemeral: (bool) Sets message invisible for other member (not author)
        :return None:
        """
        _payload = {}
        content = ""

        if list(args):
            for i in list(args):
                content += str(i) + sep
            content = content[0 : len(content) - len(sep)]

        if ephemeral:
            if action_row:
                _payload = {
                    "type": 4,
                    "data": {
                        "content": content,
                        "flags": _MessageFlags.EPHEMERAL,
                        "components": action_row.json,
                    },
                }
            else:
                _payload = {
                    "type": 4,
                    "data": {"content": content, "flags": _MessageFlags.EPHEMERAL},
                }
        else:
            if action_row:
                _payload = {
                    "type": 4,
                    "data": {"content": content, "components": action_row.json},
                }
            else:
                _payload = {"type": 4, "data": {"content": content}}

        _id = self._interaction_id
        _token = self._interaction_token

        _url = f"https://discord.com/api/v10/interactions/{_id}/{_token}/callback"

        await _SendingRestHandler.execute(_url, _payload, self._t)

    async def send_modal(self, title: str, custom_id: str, action_row: ActionRow):
        """send_modal()

        Args:
            title (str): Title of modal
            custom_id (str): Custom id of modal
            action_row (ActionRow): Action row with components for modal
        """
        _payload = {
            "type": 9,
            "data": {
                "title": title,
                "custom_id": custom_id,
                "components": action_row.json,
            },
        }

        _id = self._interaction_id
        _token = self._interaction_token

        _url = f"https://discord.com/api/v10/interactions/{_id}/{_token}/callback"

        await _SendingRestHandler.execute(_url, _payload, self._t)
