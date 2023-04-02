'''
Utils for simpler developerment pytecord
'''

from typing import TYPE_CHECKING, Any, TypeVar, Literal

from pytecord.enums import GatewayOpcode, MessageFlags
from pytecord.profiles import User
from pytecord.channel import Channel
from pytecord.route import Route

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from pytecord.annotations import Strable, Snowflake

KT = TypeVar('KT')
VT = TypeVar('VT')

def auth(token: str):
    '''
    Auth the user with token
    '''
    return {
        'Authorization': f'Bot {token}',
        'content-type': 'application/json',
    }

def get_token_from_auth(hdrs: dict[str, Any]):
    '''
    Get token from auth headers
    '''
    return hdrs['Authorization'].split(' ')[1]

def get_hook_debug_message(data: dict) -> str:
    '''
    Get webhook debuging message
    '''
    res = f"S{data.get('s', '')} "

    if data.get('op') == GatewayOpcode.dispatch:
        res += data.get('t', '')
    else:
        res += f"OP{data.get('op', 0)}"

    res += f" | {str(data.get('d', {}))}"
    return res

def message_payload(*strings: list['Strable'], sep: str = ' ', ephemeral: bool = False, tts: bool = False) -> dict[str, Any]:
    content = ''
    for i in strings:
        content += (str(i) + sep)
    content = content.removesuffix(sep)

    embeds = None # TODO: Add embed support
    allowed_mentions = None # TODO: Add allowed mentions support
    flags = MessageFlags.ephemeral if ephemeral else 0

    return {
        'tts': tts,
        'content': content,
        'embeds': embeds,
        'allowed_mentions': allowed_mentions,
        'flags': flags,
    }

def get(__type: Literal['channel', 'user'], __id: 'Snowflake', __token: str, __session: 'ClientSession') -> Channel | User:
    endpoint = '/'

    match __type:
        case 'channel':
            endpoint += 'channels'
        case 'user':
            endpoint += 'users'
    endpoint += f'/{__id}'

    data, _ = Route(endpoint, method='GET', token=__token).request()

    types = {
        'channel': Channel,
        'user': User
    }
    return types.get(__type)(__session, **data)

def get_channel(__id: 'Snowflake', __token: str, __session: 'ClientSession') -> Channel:
    return get('channel', __id, __token, __session)

def get_user(__id: 'Snowflake', __token: str, __session: 'ClientSession') -> User:
    return get('user', __id, __token, __session)
