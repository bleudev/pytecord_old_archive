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
from typing import (
    List,
    Optional
)

__all__: tuple = ("Color", "Field", "Embed")


class Color:
    """
    Colors for embeds
    """

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

    @staticmethod
    def from_hex(hex_color: str):
        """from_hex
        Return color from hex

        Args:
            hex_color (str): Color in HEX form (example, #FFFFFF)

        Raises:
            RuntimeError: Invalid hex

        Returns:
            int: color
        """
        if hex_color.startswith("#"):
            hex_color = hex_color.replace("#", "")

            if hex_color.isdigit():
                return int(hex_color, 16)

            raise RuntimeError(f"Invalid hex! #{hex_color} is not hex")

        raise RuntimeError("Invlid hex! (It needs start from #)")


class Field:
    """
    Fields for embeds
    """

    def __init__(self, name: str, value: str, inline: bool = True):
        self.name = name
        self.value = value
        self.inline = inline

    def set_name(self, new_name: str):
        """set_name
        Set new name to field

        Args:
            new_name (str): New name
        """
        self.name = new_name

    def set_value(self, new_value: str):
        """set_value
        Set new value to field

        Args:
            new_value (str): New value
        """
        self.value = new_value

    def set_inline(self, new_inline: bool):
        """set_inline
        Set new inline value to field

        Args:
            new_inline (bool): new inline value
        """
        self.inline = new_inline


class _SpriteComponents:
    def __init__(self) -> None:
        self.image: dict = None
        self.thumbnail: dict = None

    def set_image(self, image: dict):
        """set_image
        Set image to sprite components

        Args:
            image (dict): Image json data
        """
        self.image = image

    def set_thumbnail(self, thumbnail: dict):
        """set_thumbnail
        Set thumbnail to sprite components

        Args:
            thumbnail (dict): Thumbnail json data
        """
        self.thumbnail = thumbnail


class Embed:
    """
    Embeds for messages
    """

    def __init__(
        self,
        title: str,
        *,
        description: str = None,
        color: int = Color.DEFAULT,
        footer: str = None,
    ) -> None:
        self.title: str = title
        self.description: str = description
        self.color: str = color
        self.footer: str = {"text": footer}
        self.author: dict = None
        self.url = None

        self.sprite_components = _SpriteComponents()

        self.fields: List[Field] = []

    def add_field(
        self,
        name: str,
        value: str,
        *,
        inline: bool = True,
        obj: Optional[Field] = None
    ) -> None:
        """add_field
        Add field to embed

        Args:
            name (str): Name of field
            value (str): Value of field
            inline (bool, optional): Field in line?. Defaults to True.
            obj (Field, optional): Field object. Defaults to None

        Returns:
            None
        """
        if obj:
            self.fields.append(obj)
            return
        self.fields.append(Field(name, value, inline))

    def set_author(
        self,
        name: str,
        url: str = None,
        icon_url: str = None,
        proxy_icon_url: str = None,
    ) -> None:
        """set_author
        Set author for embed

        Args:
            name (str): Name of author
            url (str, optional): Url of author. Defaults to None.
            icon_url (str, optional): Icon url of author. Defaults to None.
            proxy_icon_url (str, optional): Proxy icon url of author. Defaults to None.

        Returns:
            None
        """
        self.author = {
            "name": name,
            "url": url,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_icon_url,
        }

    def set_thumbnail(
        self, url: str, proxy_url: str = None, height: int = None, width: int = None
    ) -> None:
        """set_thumbnail
        Set thumbnail for embed

        Args:
            url (str): Url of thumbnail
            proxy_url (str, optional): Proxy url of thumbnail. Defaults to None.
            height (int, optional): Height of thumbnail. Defaults to None.
            width (int, optional): Width of thumbnail. Defaults to None.

        Returns:
            None
        """
        self.sprite_components.set_thumbnail(
            {"url": url, "proxy_url": proxy_url, "height": height, "width": width}
        )

    def set_image(
        self, url: str, proxy_url: str = None, height: int = None, width: int = None
    ) -> None:
        """set_image
        Set image for embed

        Args:
            url (str): Url of image_
            proxy_url (str, optional): Proxy url of image. Defaults to None.
            height (int, optional): Height of image Defaults to None.
            width (int, optional): Width of image. Defaults to None.

        Returns:
            None
        """
        self.sprite_components.set_image(
            {"url": url, "proxy_url": proxy_url, "height": height, "width": width}
        )

    def tojson(self) -> dict:
        """tojson
        Return json data of embed

        Returns:
            dict: Json data
        """
        fields_jsons = []

        for field in self.fields:
            fields_jsons.append(field.tojson())

        embed_json = {
            "title": self.title,
            "description": self.description,
            "footer": self.footer,
            "color": self.color,
            "fields": fields_jsons,
            "author": self.author,
            "thumbnail": self.sprite_components.thumbnail,
            "image": self.sprite_components.image,
        }

        return embed_json
