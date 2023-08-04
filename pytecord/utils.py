import json
from typing import Any

from aiohttp import ClientSession
from requests import get

from .config import API_VERSION

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

    def eval(self) -> dict[str, Any]:
        return json.dumps(self.json)


def get_headers(token: str):
    return {'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}

def rget(endpoint: str, token: str = None, headers: dict[str, Any] = None):
    if token:
        headers = get_headers(token)
    return get(f'https://discord.com/api/v{API_VERSION}{endpoint}', headers=headers)

async def apost(endpoint: str, token: str = None, headers: dict[str, Any] = None, data: dict[str, Any] = None):
    if token:
        headers = get_headers(token)
    async with ClientSession(headers=headers) as s:
        async with s.post(f'https://discord.com/api/v{API_VERSION}{endpoint}', data=data) as r:
            if r.status == 200:
                return  await r.json()
            raise Exception(await r.json())

# OTHER

def get_snowflake(__snowflake: str, __default: Any = None) -> int | Any:
    """
    Get snowflake from string. `__snowflake` argument is string,
    `__default` is a default which is using in situations when
    `bool(__snowflake)` is `False`
    """
    return int(x) if (x := __snowflake) else __default

def check_module(module: str):
    try:
        __import__(module)
    except ImportError:
        return False
    return True
