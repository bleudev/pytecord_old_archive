import json
from typing import Any, TypeVar

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from requests import get

from .config import API_VERSION
from .enums import ApplicationCommandOptionType
from .timestamp import Timestamp
from .annotations import hex_str, height, width

T = TypeVar('T')


class DiscordException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


# API/GATEWAY

class Color:
    @staticmethod
    def black() -> 'Color':
        return Color('000000')

    @staticmethod
    def white() -> 'Color':
        return Color('ffffff')
    
    @staticmethod
    def red() -> 'Color':
        return Color('ff0000')
    
    @staticmethod
    def green() -> 'Color':
        return Color('00ff00')
    
    @staticmethod
    def blue() -> 'Color':
        return Color('0000ff')

    def __init__(self, hex_str: hex_str) -> None:
        hex_str = hex_str.replace('#', '')
        hex_str = hex_str.lower()

        if len(hex_str) == 6:
            self.hex_str = hex_str # in this format: FFFFFF
        else:
            self.hex_str = None
    
    def __str__(self) -> str:
        return self.hex_str

    def __int__(self) -> int:
        return int(str(self), 16)

class EmbedFooter:
    def __init__(self, text: str, icon_url: str = None, proxy_icon_url: str = None) -> None:
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url
    
    def eval(self) -> dict[str, Any]:
        return {
            'text': self.text,
            'icon_url': self.icon_url,
            'proxy_icon_url': self.proxy_icon_url
        }

class EmbedImage:
    def __init__(
            self, url: str, proxy_url: str = None,
            resolution: tuple[height, width] = [None, None]
        ) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height, self.width = resolution
    
    def eval(self) -> dict[str, Any]:
        return {
            'url': self.url,
            'proxy_url': self.proxy_url,
            'height': self.height,
            'width': self.width
        }

class EmbedThumbnail:
    def __init__(
            self, url: str, proxy_url: str = None,
            resolution: tuple[height, width] = [None, None]
        ) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height, self.width = resolution
    
    def eval(self) -> dict[str, Any]:
        return {
            'url': self.url,
            'proxy_url': self.proxy_url,
            'height': self.height,
            'width': self.width
        }

class EmbedVideo:
    def __init__(
            self, url: str = None, proxy_url: str = None,
            resolution: tuple[height, width] = [None, None]
        ) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height, self.width = resolution
    
    def eval(self) -> dict[str, Any]:
        return {
            'url': self.url,
            'proxy_url': self.proxy_url,
            'height': self.height,
            'width': self.width
        }

class EmbedProvider:
    def __init__(self, name: str = None, url: str = None) -> None:
        self.name = name
        self.url = url
    
    def eval(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'url': self.url
        }

class EmbedAuthor:
    def __init__(self, name: str, url: str = None, icon_url: str = None, proxy_icon_url: str = None) -> None:
        self.name = name
        self.url = url
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url
    
    def eval(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'url': self.url,
            'icon_url': self.icon_url,
            'proxy_icon_url': self.proxy_icon_url
        }

class Field:
    def __init__(self, name: str, value: str, inline: bool = True) -> None:
        self.name = name
        self.value = value
        self.inline = inline
    
    def eval(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'value': self.value,
            'inline': self.inline
        }

class Embed:
    def __init__(
            self, title: str = None, description: str = None, url: str = None,
            timestamp: Timestamp = None, color: hex_str | Color = 'ffffff',
            footer: EmbedFooter = None, image: EmbedImage = None,
            thumbnail: EmbedThumbnail = None, video: EmbedVideo = None,
            provider: EmbedProvider = None, author: EmbedAuthor = None,
            fields: list[Field] = None
        ) -> None:
        self.title = title
        self.type = 'rich'
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = Color(color) if isinstance(color, str) else color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields = fields

    def eval(self) -> dict[str, Any]:
        return {
            'title': self.title,
            'type': 'rich',
            'description': self.description,
            'url': self.url,
            'timestamp': self.timestamp.to_iso(),
            'color':  int(self.color),
            'footer': self.footer.eval(),
            'image': self.image.eval(),
            'thumbnail': self.thumbnail.eval(),
            'video': self.video.eval(),
            'provider': self.provider.eval(),
            'author': self.author.eval(),
            'fields': [i.eval() for i in self.fields]
        }

class MessagePayload:
    def __init__(self, content: str) -> None:
        self.json = {
            'content': str(content)
        }
    
    def make_reply(self, message_id: int) -> None:
        self.json['message_reference'] = {
            'message_id': message_id
        }
    
    def __setitem__(self, key: str, value: Any):
        self.json[key] = value
    
    def __getitem__(self, key: str):
        return self.json[key]

    def eval(self) -> dict[str, Any]:
        return self.json


def get_headers(token: str):
    return {'Authorization': f'Bot {token}', 'content-Type': 'application/json'}

def rget(endpoint: str, token: str = None, payload: dict[str, Any] = None, headers: dict[str, Any] = None):
    if token:
        headers = get_headers(token)
    
    resp = get(f'https://discord.com/api/v{API_VERSION}{endpoint}', headers=headers, json=payload)

    if str(resp.status_code).startswith('2'):
        return resp
    else:
        raise DiscordException(resp.json())

async def apost(endpoint: str, token: str = None, headers: dict[str, Any] = None, data: dict[str, Any] = None):
    if token:
        headers = get_headers(token)
    async with ClientSession(headers=headers) as s:
        async with s.post(f'https://discord.com/api/v{API_VERSION}{endpoint}', json=data) as r:
            if str(r.status).startswith('2'):
                try:
                    return await r.json()
                except ContentTypeError:
                    return None
            raise DiscordException(await r.json())

async def adelete(endpoint: str, token: str = None, headers: dict[str, Any] = None):
    if token:
        headers = get_headers(token)
    async with ClientSession(headers=headers) as s:
        async with s.delete(f'https://discord.com/api/v{API_VERSION}{endpoint}') as r:
            if str(r.status).startswith('2'):
                try:
                    return await r.json()
                except ContentTypeError:
                    return None
            raise DiscordException(await r.json())

# OTHER

def get_snowflake(__snowflake: str, __default: Any = None) -> int | Any:
    """
    Get snowflake from string. `__snowflake` argument is string,
    `__default` is a default which is using in situations when
    `bool(__snowflake)` is `False`
    """
    return int(x) if (x := __snowflake) else __default

def get_list_of_types(__type: T, __list: list[Any], *args, __default: Any = None) -> list[T]:
    return [__type(i, *args) for i in __list] if __list else __default


def get_option_type(__annotation: type) -> int:
    option_types = {
        'SUB_COMMAND': ...,
        'SUB_COMMAND_GROUP': ...,
        str: ApplicationCommandOptionType.STRING,
        int: ApplicationCommandOptionType.INTEGER,
        bool: ApplicationCommandOptionType.BOOLEAN,
        'USER': ...,
        'CHANNEL': ...,
        'ROLE': ...,
        'MENTIONABLE': ...,
        'NUMBER': ...,
        'ATTACHMENT': ...
    }

    return option_types[__annotation]


def check_module(module: str):
    try:
        __import__(module)
    except ImportError:
        return False
    return True
