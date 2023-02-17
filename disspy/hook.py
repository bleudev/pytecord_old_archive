'''
Webhook for connection to Discord Gateway
'''

from asyncio import create_task, gather
from asyncio import sleep as async_sleep
from dataclasses import dataclass, field
from datetime import datetime
from time import mktime

from disspy import utils
from disspy.app import AppClient, Context
from disspy.channel import Channel, Message, RawMessage
from disspy.enums import ApplicationCommandType, InteractionType
from disspy.listener import Listener
from disspy.profiles import User

gateway_version = 10 # pylint: disable=invalid-name

@dataclass
class _GatewayEvent:
    op: int # pylint: disable=invalid-name
    d: dict = field(default_factory=dict) # pylint: disable=invalid-name
    s: int = 0 # pylint: disable=invalid-name
    t: str = 'NONE' # pylint: disable=invalid-name

class Hook:
    '''
    Webhook for connection to Discord Gateway
    '''
    def __init__(self, *, token: str, **options) -> None:
        self.token = token
        self.status = 'online'

        self._headers = {
            "Authorization": f"Bot {token}",
            "content-type": "application/json",
        }
        self._session = None
        self._ws = None
        self._intents = 0
        self._debug = options.get('debug', False)
        self._listener = None
        self._user_id = None
        self._app_client = None

    def _debuging(self, data: dict):
        if self._debug:
            print(utils.get_hook_debug_message(data))

    async def _get(self) -> dict:
        try:
            j = await self._ws.receive_json()
            self._debuging(j)
            return j
        except TypeError:
            return

    async def _send(self, data: dict) -> dict:
        await self._ws.send_json(data)
        self._debuging(data)
        return data

    async def _identify(self) -> dict:
        j = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self._intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "disspy",
                    "$device": "disspy"
                },
                "presence": {
                    "since": mktime(datetime.now().timetuple()) * 1000,
                    "afk": False,
                    "status": self.status,
                    "activities": [] # Not supported
                }
            }
        }
        return await self._send(j)

    async def run(self, _session, listener: Listener, app_client: AppClient, **options):
        '''
        Run the hook
        '''
        self._intents = options.get('intents', 0)
        self._session = _session
        self._listener = listener
        self._app_client = app_client

        async with self._session.ws_connect(
            f"wss://gateway.discord.gg/?v={gateway_version}&encoding=json"
        ) as _ws:
            self._ws = _ws

            data = await self._get()
            await self._identify()

            await gather(
                create_task(self._life(data['d']['heartbeat_interval'] / 1000)),
                create_task(self._events())
            )

    async def _register_app_commands(self, app_id):
        for i in self._app_client.commands:
            await self._session.post(
                f'https://discord.com/api/v10//applications/{app_id}/commands',
                json=i.eval()
            )

    async def _life(self, interval):
        while True:
            await self._send({"op": 1, "d": None, "t": None})

            await async_sleep(interval)

    async def _events(self):
        while True:
            if x := await self._get(): # pylint: disable=invalid-name
                event = _GatewayEvent(**x)
            else:
                continue

            match event.t:
                case 'READY':
                    self._user_id = event.d['user']['id']
                    await self._register_app_commands(event.d['application']['id'])
                    await self._listener.invoke_event('ready')
                case 'MESSAGE_CREATE' | 'MESSAGE_UPDATE':
                    if event.d['author']['id'] != self._user_id:
                        message = Message(self._session, **event.d)
                        await self._listener.invoke_event('message', message)
                case 'MESSAGE_DELETE':
                    raw_message = RawMessage(self._session, **event.d)
                    await self._listener.invoke_event('message_delete', raw_message)
                case 'INTERACTION_CREATE':
                    ctx = Context(event.d, self.token, self._session, self)

                    interaction_type = event.d['type']

                    if interaction_type is InteractionType.application_command:
                        command_data: dict = event.d['data']
                        command_type: int = command_data['type']
                        command_name: str = command_data['name']

                        if command_type is ApplicationCommandType.chat_input:
                            option_values = {}
                            if command_data.get('options', None):
                                option_jsons = command_data['options']
                                resolved = command_data.get('resolved')

                                for option_json in option_jsons:
                                    _type = option_json['type']
                                    if _type in [6, 7]:
                                        target_id = option_json['value']

                                        resolved_types = {
                                            6: 'users',
                                            7: 'channels'
                                        }
                                        resolved_data = resolved[resolved_types[_type]][target_id]

                                        _types = {
                                            6: User,
                                            7: Channel
                                        }

                                        option_values.setdefault(
                                            option_json['name'],
                                            _types[_type](self._session, **resolved_data)
                                        )
                                    else:
                                        option_values.setdefault(
                                            option_json['name'],
                                            option_json['value']
                                        )

                            if option_values:
                                await self._app_client.invoke_command(
                                    command_name, command_type,
                                    ctx, **option_values)
                            else:
                                await self._app_client.invoke_command(
                                    command_name, command_type,
                                    ctx)
                        else:
                            resolved_data = command_data['resolved']
                            target_id = command_data['target_id']

                            if command_type is ApplicationCommandType.user:
                                resolved = User(self._session, **resolved_data['users'][target_id])
                            elif command_type is ApplicationCommandType.message:
                                resolved = Message(
                                    self._session, **resolved_data['messages'][target_id])
                            await self._app_client.invoke_command(
                                command_name, command_type,
                                ctx, resolved)
                    elif interaction_type == InteractionType.modal_submit:
                        submit_data = event.d['data']
                        inputs_values = {}

                        for i in submit_data['components']:
                            text_input = i['components'][0]

                            if text_input['value']:
                                inputs_values.setdefault(
                                    text_input['custom_id'],
                                    text_input['value']
                                )

                        await self._app_client.invoke_modal_submit(
                            submit_data['custom_id'],
                            ctx,
                            **inputs_values
                        )
                case _:
                    if self._debug:
                        print(f'Unknown {event.t} event type!')
