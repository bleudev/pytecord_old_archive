'''
Utils for simpler developerment disspy
'''

from disspy.enums import GatewayOpcode


def auth(token: str):
    '''
    Auth the user with token
    '''
    return {
        'Authorization': f'Bot {token}',
        'content-type': 'application/json',
    }

def get_token_from_auth(hdrs: dict):
    '''
    Get token from auth headers
    '''
    return hdrs['Authorization'].split(' ')[1]

def get_content(*args, sep):
    '''
    Get content for message
    '''
    result = ''

    for i in args:
        result += (str(i) + sep)
    result = result.removesuffix(sep)

    return result

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
