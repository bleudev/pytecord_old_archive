import json
from typing import Any, TypeVar

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from requests import get

from .config import API_VERSION
from .enums import ApplicationCommandOptionType

T = TypeVar('T')


class DiscordException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


# API/GATEWAY

class MessagePayload:
    def __init__(self, content: str) -> None:
        self.json = {
            'content': content
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

def rget(endpoint: str, token: str = None, headers: dict[str, Any] = None):
    if token:
        headers = get_headers(token)
    
    resp = get(f'https://discord.com/api/v{API_VERSION}{endpoint}', headers=headers)

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
