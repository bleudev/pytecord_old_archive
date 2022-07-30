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

# Imports
from random import random
from math import floor
from typing import NoReturn

__all__: tuple = (
    "DisColor",
    "DisField",
    "DisEmbed"
)


class DisColor:
    """DisColor
    Colors for embeds
    """

    __classname__ = "DisColor"

    DEFAULT = 0
    AQUA = 1752220
    DARK_AQUA = 1146986
    GREEN = 3066993
    DARK_GREEN = 2067276
    BLUE = 3447003
    DARK_BLUE = 2123412
    PURPLE = 10181046
    DARK_PURPLE = 7419530
    LUMINOUS_VIVID_PINK = 15277667
    DARK_VIVID_PINK = 11342935
    GOLD = 15844367
    DARK_GOLD = 12745742
    ORANGE = 15105570
    DARK_ORANGE = 11027200
    RED = 15158332
    DARK_RED = 10038562
    GREY = 9807270
    DARK_GREY = 9936031
    DARKER_GREY = 8359053
    LIGHT_GREY = 12370112
    NAVY = 3426654
    DARK_NAVY = 2899536
    YELLOW = 16776960
    WHITE = 16777215
    BLURPLE = 5793266
    GREYPLE = 10070709
    DARK_BUT_NOT_BLACK = 2895667
    NOT_QUITE_BLACK = 2303786
    OFFICIAL_GREEN = 5763719
    OFFICIAL_YELLOW = 16705372
    FUSCHIA = 15418782
    BLACK = 2303786
    OFFICIAL_RED = 15548997

    @staticmethod
    def random():
        """RANDOM
        Generate random color

        Returns:
            int: Random color
        """
        return floor(random() * 16777214) + 1


class DisField:
    """DisField
    Fields for embeds
    """
    def __init__(self, name: str, value: str, inline: bool = True):
        self.name = name
        self.value = value
        self.inline = inline


class DisEmbed:
    """DisEmbed
    Embeds for messages
    """
    def __init__(self, title: str, description: str = None, color=0xffffff, footer: str = None):
        self.title: str = title
        self.description: str = description
        self.color: str = color
        self.footer: str = footer
        self.author: dict = None
        self.image: dict = None
        self.thumbnail: dict = None

        self.fields: list[DisField] = []

    def add_field(self, title: str, value: str) -> NoReturn:
        self.fields.append(DisField(title, value))

    def add_field_from_obj(self, field: DisField) -> NoReturn:
        self.fields.append(field)

    def set_author(self, name: str, url: str = None, icon_url: str = None,
                   proxy_icon_url: str = None) -> NoReturn:
        """
        Set author for embed
        """
        self.author = {
            "name": name,
            "url": url,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_icon_url
        }

    def set_thumbnail(self, url: str, proxy_url: str = None, height: int = None, width: int = None):
        """
        Set thumbnail for embed
        """
        self.thumbnail = {
            "url": url,
            "proxy_url": proxy_url,
            "height": height,
            "width": width
        }

    def set_image(self, url: str, proxy_url: str = None, height: int = None, width: int = None):
        """
        Set image for embed
        """
        self.image = {
            "url": url,
            "proxy_url": proxy_url,
            "height": height,
            "width": width
        }

    def tojson(self):
        fields_jsons = []

        for f in self.fields:
            fields_jsons.append(f.tojson())

        embed_json = {
            "title": self.title,
            "description": self.description,
            "footer": self.footer,
            "color": self.color,
            "fields": fields_jsons,
            "author": self.author
        }

        return embed_json
