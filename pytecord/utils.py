from requests import get, post
from aiohttp import ClientSession
import json

from typing import Literal, Any

from .config import API_VERSION

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
