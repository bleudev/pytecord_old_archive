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
    Dict
)


class Component:
    def __init__(self, ctype, custom_id=None, label=None, style=None, url=None, min_length=None, max_length=None, placeholder=None, required=None) -> NoReturn:
        if ctype == 1:
            print("Action Rows don't can to use by users")
        else:
            if ctype == 2:
                if not style == 5 and url and not custom_id or style == 5 and not url and custom_id:
                    print("Error!")
                else:
                    self.type = ctype
                    self.custom_id = custom_id
                    self.label = label
                    self.style = style
                    self.url = url
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
    def __init__(self,  label, style, url=None, custom_id=None,) -> NoReturn:
        if not style == 5 and url and not custom_id or style == 5 and not url and custom_id:
            print("Error!")
        else:
            super().__init__(2, custom_id, label, style, url)


class ButtonStyle:
    BLUE = 1
    GREY = 2
    GREEN = 3
    RED = 4
    LINK = 5


class TextInput(Component):
    def __init__(self, label, style, min_length, max_length, placeholder, required=False):
        super().__init__(4, custom_id=label, style=style, label=label, min_length=min_length, max_length=max_length,
                         placeholder=placeholder, required=required)


class _ComponentGenerator:
    def __new__(cls, c: Component) -> Dict:
        if c.type == 2:
            return {
                "type": c.type,
                "custom_id": c.custom_id,
                "label": c.label,
                "style": c.style,
                "url": c.url
            }
        elif c.type == 4:
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
    def __init__(self, bot) -> NoReturn:
        self.json = [{
            "type": 1,
            "components": []
        }]
        self._b = bot

    def add(self, c: Component):
        def wrapper(func):
            self.json[0]["components"].append(_ComponentGenerator(c))
            from disspy.client import DisBot
            self._b: DisBot = self._b
            self._b.api.comsevs[c.custom_id] = func

        return wrapper
