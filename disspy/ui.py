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
    NoReturn,
    Dict,
    Optional,
    Text,
    Union
)

from disspy.reaction import DisEmoji
from disspy import errors


class Component:
    """
    Class for creating components
    """
    def __init__(self, ctype, custom_id=None, label=None, style=None, url=None,
                 options=None, min_values=None, max_values=None,
                 min_length=None, max_length=None, placeholder=None, required=None) -> NoReturn:
        if ctype == 1:
            raise errors.MessageComponentIsBlocked("Action Rows don't can to use by users")
        else:
            if ctype == 2:
                if not style == 5 and url and not custom_id or style == 5 and not url and custom_id:
                    raise RuntimeError("Error with creating components!")
                else:
                    self.type = ctype
                    self.custom_id = custom_id
                    self.label = label
                    self.style = style
                    self.url = url
            elif ctype == 3:
                self.type = ctype
                self.custom_id = custom_id
                self.options = options
                self.min_values = min_values
                self.max_values = max_values
                self.placeholder = placeholder
            elif ctype == 4:
                self.type = ctype
                self.style = style
                self.label = label
                self.custom_id = custom_id
                self.min_length = min_length
                self.max_length = max_length
                self.placeholder = placeholder
                self.required = required


class Button(Component):
    """
    Class for creating buttons in Action Row
    """
    def __init__(self, label: Text, style: Optional[int] = None, url: Optional[str] = None,
                 custom_id: Optional[Text] = None, ) -> NoReturn:
        if not style == 5 and url and not custom_id or style == 5 and not url and custom_id:
            raise RuntimeError("Error with creating buttons!")
        else:
            if style is None:  # Default
                style = 1  # Blue
            super().__init__(2, custom_id, label, style, url)


class ButtonStyle:
    """
    Button styles from official discord docs
    """
    BLUE = 1
    GREY = 2
    GREEN = 3
    RED = 4
    LINK = 5


class SelectMenuOption:
    """
    Class for creating options in select menus
    """
    def __init__(self, label: str, value: str, description: str, emoji: Union[DisEmoji, str],
                 default: bool = False) -> NoReturn:
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def json(self) -> Dict:
        """json()

        Returns:
            Dict: Json data of option
        """
        if isinstance(self.emoji, DisEmoji):
            if self.emoji.unicode:
                e_j = {
                    "name": self.emoji.unicode,
                    "id": self.emoji.emoji_id
                }
            else:
                e_j = {
                    "name": self.emoji.name,
                    "id": self.emoji.emoji_id
                }
        else:
            e_j = {
                "name": self.emoji,
                "id": None
            }

        return {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "emoji": e_j,
            "default": self.default
        }


class SelectMenu(Component):
    """
    Class for creating select menus in Action Row
    """
    def __init__(self, custom_id: str, options: list[SelectMenuOption], placeholder: str,
                 min_values: int, max_values: int) -> NoReturn:
        oj = []

        for i in options:
            oj.append(i.json())

        super().__init__(3, custom_id=custom_id, options=oj, min_values=min_values,
                         max_values=max_values, placeholder=placeholder)


class TextInput(Component):
    """
    Class for creating text inputs in Action Row
    """
    def __init__(self, label, min_length, max_length, placeholder,
                 required=False, style=None) -> NoReturn:
        if style is None:  # Default
            style = 1  # Short
        super().__init__(4, custom_id=label, style=style, label=label,
                         min_length=min_length, max_length=max_length,
                         placeholder=placeholder, required=required)


class TextInputStyle:
    """
    Text input styles from official discord docs
    """
    SHORT = 1
    PARAGRAPH = 2


class _ComponentGenerator:
    def __new__(cls, c: Component) -> Dict:
        if c.type == 2:  # Buttons
            return {
                "type": c.type,
                "custom_id": c.custom_id,
                "label": c.label,
                "style": c.style,
                "url": c.url
            }
        elif c.type == 3:  # Select Menu
            return {
                "type": c.type,
                "custom_id": c.custom_id,
                "min_values": c.min_values,
                "max_values": c.max_values,
                "placeholder": c.placeholder,
                "options": c.options
            }
        elif c.type == 4:  # Text Input
            return {
                "type": c.type,
                "custom_id": c.custom_id,
                "style": c.style,
                "label": c.label,
                "min_length": c.min_length,
                "max_length": c.max_length,
                "placeholder": c.placeholder,
                "required": c.required
            }


class ActionRow:
    """
    Class for creating action rows in messages
    """
    def __init__(self, bot) -> NoReturn:
        self.json = [{
            "type": 1,
            "components": []
        }]
        self._b = bot

    def add(self, c: Component):
        """add()

        Args:
            c (Component): Component
        """
        def wrapper(func):
            self.json[0]["components"].append(_ComponentGenerator(c))
            self._b = self._b
            self._b.api.comsevs[c.custom_id] = func

        return wrapper
