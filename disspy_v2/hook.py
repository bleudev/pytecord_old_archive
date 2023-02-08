from asyncio import gather, create_task
from asyncio import sleep as async_sleep

from datetime import datetime
from time import mktime
from json import dumps

from disspy_v2.listener import Listener
from disspy_v2.channel import Message, RawMessage, Channel
from disspy_v2.app import AppClient, Context
from disspy_v2.profiles import User
from disspy_v2.enums import InteractionType, ApplicationCommandType
from disspy_v2 import utils

gateway_version = 10

class _Gateway_Event:
    def __init__(self, **_dict) -> None:
        self.op = _dict.get('op', 0)
        self.data = _dict.get('d', {})
        self.session = _dict.get('s', 0)
        self.type = _dict.get('t', 'NONE')


class Hook:
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

    async def _get(self) -> dict:
        try:
            j = await self._ws.receive_json()
        except TypeError:
            return
        return j

    async def _send(self, data: dict) -> dict:
        await self._ws.send_json(data)
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
            interval = data["d"]["heartbeat_interval"] / 1000

            await self._identify()

            tasks = [
                create_task(self._life(interval)),
                create_task(self._events()),
            ]
            await gather(*tasks)

    def _debuging(self, data: dict):
        if self._debug:
            mes = utils.get_hook_debug_message(data)
            print(mes)

    async def _register_app_commands(self, app_id):
        command_jsons = []
        for i in self._app_client.commands:
            command_jsons.append(i.eval())
        url = f'https://discord.com/api/v10//applications/{app_id}/commands'
        for c in command_jsons:
            async with self._session.post(url, data=dumps(c)) as r:
                j = await r.json()
                if self._debug:
                    print('POST |', j)

    async def _life(self, interval):
        while True:
            j = {"op": 1, "d": None, "t": None}
            await self._send(j)

            self._debuging(j)

            await async_sleep(interval)

    async def _events(self):
        while True:
            _data = await self._get()
            
            if _data:
                event = _Gateway_Event(**_data)
            else:
                continue
            self._debuging(_data)

            if event.type == 'READY':
                self._user_id = event.data['user']['id']

                await self._register_app_commands(event.data['application']['id'])

                await self._listener.invoke_event('ready')
            if event.type in ['MESSAGE_CREATE', 'MESSAGE_UPDATE']:
                message_data = event.data

                if message_data['author']['id'] != self._user_id:
                    message = Message(self._session, **message_data)
                    await self._listener.invoke_event('message', message)
            if event.type == 'MESSAGE_DELETE':
                raw_message = RawMessage(self._session, **event.data)
                await self._listener.invoke_event('message_delete', raw_message)
            if event.type == 'INTERACTION_CREATE':
                ctx = Context(event.data, self.token, self._session, self)

                if event.data['type'] == InteractionType.application_command:
                    if event.data['data']['type'] == ApplicationCommandType.chat_input:
                        option_values = {}
                        if event.data['data'].get('options', None):
                            option_jsons = event.data['data']['options']
                            resolved = event.data['data'].get('resolved')
                            
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
                            await self._app_client.invoke_command(event.data['data']['name'], event.data['data']['type'], ctx, **option_values)
                        else:
                            await self._app_client.invoke_command(event.data['data']['name'], event.data['data']['type'], ctx)
                    else:
                        _data = event.data['data']
                        _type = _data['type']
                        resolved = None
                        target_id = _data['target_id']
                        if _type == 2: # Users
                            _resolved_data = _data['resolved']['users'][target_id]
                            resolved = User(self._session, **_resolved_data)
                        elif _type == 3: # Message
                            _resolved_data = _data['resolved']['messages'][target_id]
                            resolved = Message(self._session, **_resolved_data)
                        await self._app_client.invoke_command(_data['name'], _type, ctx, resolved)
                elif event.data['type'] == InteractionType.modal_submit:
                    _data = event.data['data']
                    inputs_values = {}

                    for i in _data['components']:
                        text_input = i['components'][0]

                        if text_input['value']:
                            inputs_values.setdefault(
                                text_input['custom_id'],
                                text_input['value']
                            )

                    await self._app_client.invoke_modal_submit(
                        _data['custom_id'],
                        ctx,
                        **inputs_values
                    )
