'''
Webhook for connection to Discord Gateway
'''

from asyncio import create_task, gather, get_event_loop
from asyncio import sleep as async_sleep
from dataclasses import dataclass, field
from datetime import datetime
from time import mktime
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from aiohttp import ClientSession

from disspy import utils
from disspy.route import Route
from disspy.app import AppClient, Context
from disspy.channel import Channel, Message, RawMessage
from disspy.enums import ApplicationCommandType, ApplicationCommandOptionType, InteractionType
from disspy.listener import Listener
from disspy.profiles import User, Member
from disspy.role import Role

gateway_version = 10 # pylint: disable=invalid-name

@dataclass
class _GatewayEvent:
    op: int # pylint: disable=invalid-name
    d: dict = field(default_factory=dict) # pylint: disable=invalid-name
    s: int = 0 # pylint: disable=invalid-name
    t: str = 'NONE' # pylint: disable=invalid-name

OV = TypeVar('OV', str, float, int, bool, Member, Channel, Role)

class _OptionSerializator:
    def __new__(cls, option: dict[str, Any], resolved: list[dict[str, Any]] | None, session: 'ClientSession') -> tuple[str, OV]:
        name = option['name']
        type = option['type']
        value = None
        
        non_resolving_types = (
            ApplicationCommandOptionType.string,
            ApplicationCommandOptionType.integer,
            ApplicationCommandOptionType.boolean,
            ApplicationCommandOptionType.number
        )
        resolving_types = {
            ApplicationCommandOptionType.user: 'members*',
            ApplicationCommandOptionType.channel: 'channels',
            ApplicationCommandOptionType.role: 'roles',
            ApplicationCommandOptionType.mentionable: 'members | roles*'
        } # * - needs additional checks
        
        resolving_python_types = {
            ApplicationCommandOptionType.user: Member,
            ApplicationCommandOptionType.channel: Channel,
            ApplicationCommandOptionType.role: Role,
            ApplicationCommandOptionType.mentionable: Member | Role
        }

        if type in non_resolving_types:
            value = option['value']
        else:
            target_id = option['value']
            if type in (
                ApplicationCommandOptionType.user, ApplicationCommandOptionType.mentionable
            ):
                def _members() -> 'Member':
                    member_data = resolved['members'][target_id]
                    user_data = resolved['users'][target_id]

                    user = User(session, **user_data)
                    return Member(session, user, **member_data)

                if type is ApplicationCommandOptionType.mentionable:
                    roles, members = resolved.get('roles', []), resolved.get('members', [])

                    if roles and not members: members = [0 for i in range(len(roles))] # pylint: disable=multiple-statements
                    elif members and not roles: roles = [0 for i in range(len(members))] # pylint: disable=multiple-statements

                    result_type = None
                    for role_id, member_id in zip(roles, members):
                        if role_id == target_id:
                            result_type = 'roles'
                            break
                        if member_id == target_id:
                            result_type = 'members'
                            break

                    if result_type == 'roles':
                        data = resolved[result_type][target_id]
                        value = Role(session, **data)
                    elif result_type == 'members':
                        value = _members()

                elif type is ApplicationCommandOptionType.user:
                    value = _members()
            else:
                resolved_type_name = resolving_types[type] # For example, 'channels'
                resolved_python_type: Member | Channel | Role = resolving_python_types[type] # For example, Channel
                data = resolved[resolved_type_name][target_id]

                value = resolved_python_type(session, **data)

        return name, value

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

    async def _get(self) -> dict | None:
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
        def _name_print(l: list[dict]):
            return [i['name'] for i in l]
        
        route = Route(
            '/applications/%s/commands', app_id,
            method='GET',
            token=self.token
        )
        server_app_commands, _ = route.request()
        code_app_commands = [i.eval() for i in self._app_client.commands]
        
        print(f'{server_app_commands=}\n\n{code_app_commands=}')
        
        # server_app_commands=[{'description': 'Clear the messages in channel', 'id': '1076244001272889384', 'application_id': '965666270500495390',
        # 'version': '1076247271341047818', 'default_permission': True, 'dm_permission': True, 'default_member_permissions': '8',
        # 'options': [{'type': 4, 'name': 'amount', 'description': 'Amount of messages to delete'}], 'type': 1, 'nsfw': False, 'name': 'clear'},
        # {'description': "Remove 'крутой' role and add 'жоски' role", 'id': '1079321809129848903', 'application_id': '965666270500495390', 'version': '1079321809129848904',
        # 'default_permission': True, 'dm_permission': True, 'default_member_permissions': None, 'options': [{'description': '…', 'type': 6, 'name': 'member', 'required': True}],
        # 'type': 1, 'nsfw': False, 'name': 'don'},
        # {'description': 'No description', 'id': '1081340498662400151', 'application_id': '965666270500495390', 'version': '1081340498662400152',
        # 'default_permission': True, 'dm_permission': True, 'default_member_permissions': None, 'options': [{'type': 9, 'required': True, 'name': 'mentionable',
        # 'description': 'User or role'}], 'type': 1, 'nsfw': False, 'name': 'test_app_command'}]
        # 
        # code_app_commands=[{'type': 1, 'name': 'test_app_command', 'description': 'No description', 'options': [{'name': 'mentionable', 'type': 9, 'required': True,
        # 'description': 'User or role'}]}]
        equals_commands = [] # to PATCH
        excess_commands = [] # to DELETE
        new_commands = [] # to POST

        for code in code_app_commands:
            for server in server_app_commands:
                if code['name'] == server['name']:
                    code['id'] = server['id']
                    equals_commands.append(code)
                else:
                    if (code not in new_commands) and (code not in equals_commands):
                        new_commands.append(code)
                    if (server not in excess_commands) and (server not in equals_commands):
                        excess_commands.append(server)
        print(f'{equals_commands=}\n\n{excess_commands=}\n\n{new_commands=}')
        
        for eq in equals_commands:
            route = Route(
                '/applications/%s/commands/%s', app_id, eq['id'],
                method='PATCH',
                payload=eq
            )
            await route.async_request(self._session, get_event_loop())
        for ex in excess_commands:
            route = Route(
                '/applications/%s/commands/%s', app_id, ex['id'],
                method='DELETE'
            )
            await route.async_request(self._session, get_event_loop())
        for nw in new_commands:
            route = Route(
                '/applications/%s/commands', app_id,
                method='POST',
                payload=nw
            )
            await route.async_request(self._session, get_event_loop())

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
                                    __name, __serialized = _OptionSerializator(option_json, resolved, self._session)
                                    option_values[__name] = __serialized

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
                    if self._debug and event.t:
                        print(f'Unknown {event.t} event type!')
