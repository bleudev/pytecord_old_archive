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
    def __init__(self, ctype, custom_id, label=None, style=None) -> NoReturn:
        if ctype == 1:
            print("Action Rows don't can to use by users")
        else:
            self.type = ctype
            self.custom_id = custom_id
            self.label = label
            self.style = style


class Button(Component):
    def __init__(self, custom_id, label, style) -> NoReturn:
        super().__init__(2, custom_id, label, style)


class _ComponentGenerator:
    def __new__(cls, c: Component) -> Dict:
        return {
            "type": c.type,
            "custom_id": c.custom_id,
            "label": c.label,
            "style": c.style
        }


class ActionRow:
    def __init__(self, bot) -> NoReturn:
        self.components = [{
            "type": 1,
            "components": []
        }]
        self._b = bot

    def add(self, c: Component):
        def wrapper(func):
            self.components[0]["components"].append(_ComponentGenerator(c))
            from disspy.client import DisBot
            self._b: DisBot = self._b
            self._b.api.comsevs[c.custom_id] = func

        return wrapper
