from requests import get, post

from typing import Literal, Any

from pytecord.config import API_VERSION

def get_headers(token: str):
    return {'Authorization': f'Bot {token}'}}

def rget(what_to_get: Literal['channel', 'guild', 'user'], id: int, token: str = None, headers: dict[str, Any] = None):
    if token:
        headers = get_headers(token)
    return get(f'https://discord.com/api/v{API_VERSION}/{what_to_get}s/{id}', headers=headers)