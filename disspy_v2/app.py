from json import dumps
from disspy_v2.utils import get_content

class Command:
    def __init__(self, data: dict) -> None:
        self.data = data
    def __getitem__(self, key: str):
        return self.data.get(key, None)
    def eval(self) -> dict:
        return self.data

class ContextMenu:
    def __init__(self, data: dict) -> None:
        self.data = data
    def __getitem__(self, key: str):
        return self.data.get(key, None)
    def eval(self) -> dict:
        return self.data

class AppClient:
    def __init__(self) -> None:
        self.commands = []
        self.callbacks = {1: {}, 2: {}, 3: {}}

    def add_command(self, command: Command | ContextMenu, callable):
        self.commands.append(command)
        self.callbacks[command['type']].setdefault(command['name'], callable)
        
    async def invoke_command(self, name: str, type: int, *args, **kwrgs):
        await self.callbacks[type][name](*args, **kwrgs)

class _Interaction:
    def __init__(self, data: dict) -> None:
        self.token = data.get('token')
        self.id = data.get('id')
        self.application_id = data.get('application_id')

class Context:
    def __init__(self, data: dict, token: str, session) -> None:
        self._token = token
        self._interaction = _Interaction(data)
        self._session = session

        self.command = Command(data['data'])

    async def _respond(self, payload: dict):
        _token, _id = self._interaction.token, self._interaction.id
        _url = f'https://discord.com/api/v10/interactions/{_id}/{_token}/callback'
        await self._session.post(_url, data=dumps(payload))

    async def send_message(self, *strings: list[str], sep: str = ' ', ephemeral: bool = False):
        await self._respond({
            'type': 4,
            'data': {
                'content': str(get_content(*strings, sep=sep)),
                'flags': 1 << 6 if ephemeral else 0
            }
        })

    async def edit_message(self, content: str):
        await self._respond({
            'type': 7,
            'data': {
                'content': str(content)
            }
        })

    async def defer(self):
        await self._respond({
            'type': 6,
            'data': {
                'flags': 1 << 6
            }
        })

def describe(**options):
    def wrapper(func):
        try:
            return options, func[1], 'describe'
        except TypeError:
            return options, func, 'describe'
    return wrapper
