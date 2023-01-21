from json import dumps
from disspy_v2 import utils
from disspy_v2.enums import InteractionType, InteractionCallbackType
from disspy_v2.ui import Modal
from aiohttp.client_exceptions import ContentTypeError

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
        self.component_callbacks = {'modals': {}}

    def add_command(self, command: Command | ContextMenu, callable):
        self.commands.append(command)
        self.callbacks[command['type']].setdefault(command['name'], callable)

    def add_modal(self, modal: Modal):
        self.component_callbacks['modals'].setdefault(modal.custom_id, modal.submit)

    async def invoke_command(self, name: str, type: int, *args, **kwrgs):
        await self.callbacks[type][name](*args, **kwrgs)

    async def invoke_modal_submit(self, custom_id: str, *args, **kwargs):
        await self.component_callbacks['modals'][custom_id](*args, **kwargs)

class _Interaction:
    def __init__(self, data: dict) -> None:
        self.token = data.get('token')
        self.id = data.get('id')
        self.type = data.get('type')
        self.application_id = data.get('application_id')

class Context:
    def __init__(self, data: dict, token: str, session, hook) -> None:
        self._token = token
        self._interaction = _Interaction(data)
        self._session = session
        self._hook = hook

        self.command = Command(data['data'])

    async def _respond(self, payload: dict):
        _token, _id = self._interaction.token, self._interaction.id
        _url = f'https://discord.com/api/v10/interactions/{_id}/{_token}/callback'
        async with self._session.post(_url, data=dumps(payload)) as r:
            try:
                return await r.json()
            except ContentTypeError:
                return await r.text()

    async def send_message(self, *strings: list[str], sep: str = ' ', ephemeral: bool = False):
        await self._respond({
            'type': 4,
            'data': {
                'content': str(utils.get_content(*strings, sep=sep)),
                'flags': 1 << 6 if ephemeral else 0
            }
        })

    async def send_modal(self, modal: Modal):
        if self._interaction.type in [
            InteractionType.ping,
            InteractionType.modal_submit
        ]:
            return # not available in discord API
        j = await self._respond({
            'type': InteractionCallbackType.modal,
            'data': modal.eval()
        })
        self._hook._app_client.add_modal(modal)

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
