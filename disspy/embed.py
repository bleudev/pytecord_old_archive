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

"""
This file was created for manage Embeds in discord and using embeds in send messages feature

Examples:
    bot = disspy.DisBot('TOKEN')
    disspy.DisChannel("ID").send(embed=disspy.DisEmbed(title='Testing'))
"""

# Imports
from random import random
from math import floor
import typing

__all__: tuple[str] = (
    "DisColor",
    "DisField",
    "DisEmbed"
)


class _DocObject:
    __description__: str = ""  # Description to class
    __doc__: str = ""  # Mini doc with using
    __varibles__: dict[str, str] = {}  # Description to varibles
    __slots__: list[str] = []  # Slots with varibles names

    _T: typing.TypeVar = None

    def __str__(self) -> str:  # Using in str()
        r = ""

        for i in self.__varibles__.keys():
            if r == "":
                r += i
            else:
                r += f", {i}"

        return r


class DisColor(_DocObject):
    _T = typing.TypeVar("DisColor")
    __description__ = "Colors for embeds"

    def __init__(self):
        self.DEFAULT = 0
        self.AQUA = 1752220
        self.DARK_AQUA = 1146986
        self.GREEN = 3066993
        self.DARK_GREEN = 2067276
        self.BLUE = 3447003
        self.DARK_BLUE = 2123412
        self.PURPLE = 10181046
        self.DARK_PURPLE = 7419530
        self.LUMINOUS_VIVID_PINK = 15277667
        self.DARK_VIVID_PINK = 11342935
        self.GOLD = 15844367
        self.DARK_GOLD = 12745742
        self.ORANGE = 15105570
        self.DARK_ORANGE = 11027200
        self.RED = 15158332
        self.DARK_RED = 10038562
        self.GREY = 9807270
        self.DARK_GREY = 9936031
        self.DARKER_GREY = 8359053
        self.LIGHT_GREY = 12370112
        self.NAVY = 3426654
        self.DARK_NAVY = 2899536
        self.YELLOW = 16776960
        self.WHITE = 16777215
        self.BLURPLE = 5793266
        self.GREYPLE = 10070709
        self.DARK_BUT_NOT_BLACK = 2895667
        self.NOT_QUITE_BLACK = 2303786
        self.OFFICIAL_GREEN = 5763719
        self.OFFICIAL_YELLOW = 16705372
        self.FUSCHIA = 15418782
        self.OFFICIAL_RED = 15548997
        self.BLACK = 2303786

    @property
    def RANDOM(self):
        return floor(random() * 16777214) + 1


class DisField:
    def __init__(self, name: str, value: str, inline: bool = True):
        self.name = name
        self.value = value
        self.inline = inline


class _EMBED:
    title: str = ""
    description: str = ""
    color: str = ""
    footer: str = ""

    fields: list[DisField] = []


class DisEmbed(_EMBED):
    def __init__(self, title: str, description: str = None, color=0xffffff, footer: str = None):
        self.title: str = title
        self.description: str = description
        self.color: str = color
        self.footer: str = footer

        self.fields: list[DisField] = []

    def add_field(self, title: str, value: str):
        self.fields.append(DisField(title, value))

    def add_field(self, field: DisField):
        self.fields.append(field)

    def tojson(self):
        fields_jsons = []

        for f in self.fields:
            fields_jsons.append(f.tojson())

        return {
            "title": self.title,
            "description": self.description,
            "footer": self.footer,
            "color": self.color,
            "fields": fields_jsons
        }
