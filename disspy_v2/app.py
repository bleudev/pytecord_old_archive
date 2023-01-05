from json import dumps

class Command:
    def __init__(self, data: dict) -> None:
        self.data = data
    def __getitem__(self, key: str):
        return self.data[key]
    def eval(self) -> dict:
        return self.data

class AppClient:
    def __init__(self) -> None:
        self.commands = []
        self.callbacks = {1: {}, 2: {}, 3: {}}

    def add_command(self, command: Command, callable):
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

    async def send_message(self, content: str, *, ephemeral: bool = False):
        _token, _id = self._interaction.token, self._interaction.id
        _url = f'https://discord.com/api/v10/interactions/{_id}/{_token}/callback'
        _payload = {
            'type': 4,
            'data': {
                'content': str(content),
                'flags': 1 << 6 if ephemeral else 0
            }
        }
        await self._session.post(_url, data=dumps(_payload))

def describe(**options):
    def wrapper(func):
        try:
            return options, func[1], 'describe'
        except TypeError:
            return options, func, 'describe'
    return wrapper
