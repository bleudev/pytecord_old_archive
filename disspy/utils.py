from disspy.enums import GatewayOpcode

def auth(token: str):
    return {
        'Authorization': f'Bot {token}',
        'content-type': 'application/json',
    }

def get_token_from_auth(hdrs: dict):
    return hdrs['Authorization'].split(' ')[1]

def get_content(*args, sep):
    result = ''

    for i in args:
        result += (str(i) + sep)
    result = result.removesuffix(sep)

    return result

def get_hook_debug_message(data: dict) -> str:
    t, s, op, d = data.get('t'), data.get('s'), data.get('op'), data.get('d')
    res = f'S{s if s else 0} '

    if op == GatewayOpcode.dispatch:
        res += f'{t}'
    else:
        res += f'OP{op}'

    if d:
        res += f' | {str(d)}'
    return res
