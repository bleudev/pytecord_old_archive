from asyncio import get_event_loop
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

from disspy import utils
from disspy.enums import InteractionCallbackType, InteractionType, MessageFlags
from disspy.route import Route
from disspy.ui import Modal

if TYPE_CHECKING:
    from aiohttp import ClientSession

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

CT = TypeVar('CT', Command, ContextMenu)
MT = TypeVar('MT', bound=Modal)

class AppClient:
    def __init__(self) -> None:
        self.commands = []
        self.callbacks = {1: {}, 2: {}, 3: {}}
        self.component_callbacks = {'modals': {}}

    def add_command(self, command: CT, callback: Callable[..., Coroutine[Any, Any, Any]]) -> CT:
        self.commands.append(command)
        self.callbacks[command['type']].setdefault(command['name'], callback)
        return command

    def add_modal(self, modal: MT) -> MT:
        self.component_callbacks['modals'].setdefault(modal.custom_id, modal.submit)
        return modal

    async def invoke_command(self, name: str, type: int, *args, **kwrgs):
        await self.callbacks[type][name](*args, **kwrgs)

    async def invoke_modal_submit(self, custom_id: str, *args, **kwargs):
        await self.component_callbacks['modals'][custom_id](*args, **kwargs)

class _Interaction:
    def __init__(self, data: dict, token: str, session: 'ClientSession') -> None:
        self.token = data.get('token')
        self.id = data.get('id')
        self.type = data.get('type')
        self.application_id = data.get('application_id')

        self._token = token
        self._session = session

    async def respond(self, payload: dict):
        route = Route(
            '/interactions/%s/%s/callback', self.id, self.token,
            method='POST',
            token=self._token,
            payload=payload
        )
        j, _ = await route.async_request(self._session, get_event_loop())
        return j


class Context:
    def __init__(self, data: dict, token: str, session: 'ClientSession', hook) -> None:
        self._token = token
        self.interaction = _Interaction(data, token, session)
        self._session = session
        self._hook = hook

        self.command = Command(data['data'])

    async def send_message(self, *strings: list[str], sep: str = ' ', ephemeral: bool = False):
        await self.interaction.respond({
            'type': InteractionCallbackType.channel_message_with_source,
            'data': {
                'content': str(utils.get_content(*strings, sep=sep)),
                'flags': MessageFlags.ephemeral if ephemeral else 0
            }
        })

    async def send_modal(self, modal: Modal):
        if self.interaction.type in [
            InteractionType.ping,
            InteractionType.modal_submit
        ]:
            return # not available in discord API
        j = await self.interaction.respond({
            'type': InteractionCallbackType.modal,
            'data': modal.eval()
        })
        self._hook._app_client.add_modal(modal)

    async def edit_message(self, *strings: list[str], sep: str = ' ', ephemeral: bool = False):
        await self.interaction.respond({
            'type': InteractionCallbackType.update_message,
            'data': {
                'content': str(utils.get_content(*strings, sep=sep)),
                'flags': MessageFlags.ephemeral if ephemeral else 0
            }
        })

def describe(**options):
    def wrapper(func):
        try:
            return options, func[1], 'describe'
        except TypeError:
            return options, func, 'describe'
    return wrapper
