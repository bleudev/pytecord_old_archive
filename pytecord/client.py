from asyncio import run as async_run
from inspect import _empty, getdoc, signature
from sys import exit as sys_exit
from typing import Any, Callable, Coroutine, Self, TypeAlias, TypeVar

from regex import fullmatch

from pytecord.app import AppClient, Command, ContextMenu
from pytecord.channel import Channel, Message
from pytecord.connection import Connection
from pytecord.enums import (ApplicationCommandOptionType,
                            ApplicationCommandType, Permissions)
from pytecord.files import Attachment
from pytecord.listener import Listener
from pytecord.logger import warning
from pytecord.profiles import Member, User
from pytecord.role import Role

SLASH_COMMAND_VALID_REGEX = r'^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$'

CT = TypeVar( 'CT', bound=Callable[..., Coroutine[Any, Any, Any]] ) 

__all__ = (
    'Mentionable',
    'Client',
)

Mentionable: TypeAlias = Member | Role

class _flags:
    default = 16
    messages = 55824
    reactions = 9232

class Client:
    '''
    Discord client.
    
    ### Magic operations
    ---

    `+=` -> Add the event to the client

    `-=` -> Remove the event from the client

    `call` -> Run the bot

    `repr()` -> Get client data (for example, commands)
    
    ```
    async def ready(): ...
    client += ready

    client -= ready # or 'ready'

    client() # equals with client.run()

    print(client) # Prints data about client
    ```
    '''
    def _resolve_options(self, **options):
        self.debug = options.get('debug', False)
    def _validate_slash_command(self, name: str):
        return bool(fullmatch(SLASH_COMMAND_VALID_REGEX, name))
    def _get_callable(self, func):
        _c = func
        try:
            func.__name__
        except AttributeError:
            _c = func[1]
        return _c

    def __init__(self, *, token: str, **options):
        self.debug = None

        self.token = token
        self._conn = Connection(token=token, **options)
        self._listener = Listener()
        self._app = AppClient()

        self._intents = 0

        self._resolve_options(**options)

    def run(self, **options):
        try:
            async_run(self._conn.run(self._listener, self._app, intents=self._intents, **options))
        except KeyboardInterrupt:
            sys_exit(1)

    def __call__(self, **options: dict[str, Any]) -> None:
        self.run(**options)

    def __repr__(self) -> str:
        events = [a for a, b in self._listener.events.items() if b is not None]
        commands = [i['name'] for i in self._app.commands]

        return f'Client(debug={self.debug}, events={events}, commands={commands})'

    def _get_options(self, option_tuples: list[tuple[str, tuple[type, Any]]]) -> list[dict]:
        option_jsons = []
        option_types = {
            'SUB_COMMAND': ApplicationCommandOptionType.sub_command,
            'SUB_COMMAND_GROUP': ApplicationCommandOptionType.sub_command_group,
            str: ApplicationCommandOptionType.string,
            int: ApplicationCommandOptionType.integer,
            bool: ApplicationCommandOptionType.boolean,
            Member: ApplicationCommandOptionType.user,
            Channel: ApplicationCommandOptionType.channel,
            Role: ApplicationCommandOptionType.role,
            Mentionable: ApplicationCommandOptionType.mentionable,
            float: ApplicationCommandOptionType.number,
            Attachment: ApplicationCommandOptionType.attachment,
        }
        for n, (t, d) in option_tuples: # pylint: disable=invalid-name
            option_jsons.append({
                'name': n,
                'type': option_types[t],
                'required': d == _empty,
            })
        return option_jsons
    
    def _get_perms(self, *perms: list[str]) -> int:
        permission_dict = {
            'create_instant_invite': Permissions.create_instant_invite,
            'kick_members': Permissions.kick_members,
            'ban_members': Permissions.ban_members,
            'administrator': Permissions.administrator,
            'manage_channels': Permissions.manage_channels,
            'manage_guild': Permissions.manage_guild,
            'add_reactions': Permissions.add_reactions,
            'view_audit_log': Permissions.view_audit_log,
            'priority_speaker': Permissions.priority_speaker,
            'stream': Permissions.stream,
            'view_channel': Permissions.view_channel,
            'send_messages': Permissions.send_messages,
            'send_tts_messages': Permissions.send_tts_messages,
            'manage_messages': Permissions.manage_messages,
            'embed_links': Permissions.embed_links,
            'attach_files': Permissions.attach_files,
            'read_message_history': Permissions.read_message_history,
            'mention_everyone': Permissions.mention_everyone,
            'use_external_emojis': Permissions.use_external_emojis,
            'view_guild_insights': Permissions.view_guild_insights,
            'connect': Permissions.connect,
            'speak': Permissions.speak,
            'mute_members': Permissions.mute_members,
            'deafen_members': Permissions.deafen_members,
            'move_members': Permissions.move_members,
            'use_vad': Permissions.use_vad,
            'change_nickname': Permissions.change_nickname,
            'manage_nicknames': Permissions.manage_nicknames,
            'manage_roles': Permissions.manage_roles,
            'manage_webhooks': Permissions.manage_webhooks,
            'manage_emojis_and_stickers': Permissions.manage_emojis_and_stickers,
            'use_application_commands': Permissions.use_application_commands,
            'request_to_speak': Permissions.request_to_speak,
            'manage_events': Permissions.manage_events,
            'manage_threads': Permissions.manage_threads,
            'create_public_threads': Permissions.create_public_threads,
            'create_private_threads': Permissions.create_private_threads,
            'use_external_stickers': Permissions.use_external_stickers,
            'send_messages_in_threads': Permissions.send_messages_in_threads,
            'use_embedded_activities': Permissions.use_embedded_activities,
            'moderate_members': Permissions.moderate_members
        }
        rperms = 0
        for i in perms:
            try:
                rperms += permission_dict[i]
            except KeyError:
                warning(f'You are using invalid permission name "{i}". This will be ignored...')
        return rperms

    def command(self, *perms: list[str]) -> Callable[..., Command]:
        """
        Create an app command

        ```
        @client.command('administrator')
        @app.describe(
            first='First argument'
        )
        async def test(ctx: Context, first: str):
            '''
            Hello!
            '''
            await ctx.send_message(first)
        ```

        Returns:
            Command: Created command
        """
        def wr(__f: Callable[..., Coroutine[Any, Any, Any]]):
            callable = self._get_callable(__f)

            command_json = {
                'type': ApplicationCommandType.chat_input,
                'name': callable.__name__,
                'default_member_permissions': self._get_perms(*perms)
            }

            # ===
            doc = getdoc(callable)

            param_index = doc.find('Params:')
            if param_index != -1:
                end_index = doc.find('---', param_index+1)
                if end_index != -1:
                    params_string = doc[param_index:end_index]
                else:
                    params_string = doc[param_index:]

            params_string = params_string.removeprefix('Params:').strip()
            params_string = params_string.replace('    ', '')
            params_descrp = params_string.splitlines()
            params_dict = {}

            for i in params_descrp: # name:description
                name, description = i.split(':', 1)
                params_dict[name] = description

            print(f'{params_dict=}')
            # ===

            description = doc.splitlines()[0] if doc else None # pylint: disable=invalid-name

            params = dict(signature(callable).parameters)
            option_tuples = [(k, (v.annotation, v.default)) for k, v in list(params.items())[1:]]
            option_jsons = self._get_options(x) if (x := option_tuples) else [] # pylint: disable=invalid-name

            if option_jsons:
                for i in option_jsons:
                    i['description'] = 'No description'

                for option in option_jsons:
                    for name, description in params_dict.items():
                        if option['name'] == name:
                            option['description'] = description

            command_json.update(
                name=callable.__name__,
                description=x if (x := description) else 'No description', # pylint: disable=invalid-name
                options=option_jsons,
            )

            if isinstance(__f, tuple):
                json, callable, string = __f
                match string:
                    case 'describe':
                        if command_json.get('options'):
                            for option in command_json.get('options'):
                                for name, description in json.items():
                                    if option['name'] == name:
                                        option['description'] = description
                    case _:
                        command_json.update(**json)

            if not self._validate_slash_command(command_json['name']):
                raise ValueError(
                    f'All slash command names must followed {SLASH_COMMAND_VALID_REGEX} regex'
                )

            print(command_json)
            command = Command(command_json)
            self._app.add_command(command, callable)
            return command
        return wr

    def _get_menu_type(self, func: Callable[..., Coroutine[Any, Any, Any]]):
        params = dict(signature(func).parameters)
        param_type = params[list(params.keys())[1]].annotation
        types = {
            User: ApplicationCommandType.user,
            Message: ApplicationCommandType.message,
        }
        return types[param_type]

    def context_menu(self) -> Callable[..., ContextMenu]:
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]) -> ContextMenu:
            menu_json = dict(
                name=func.__name__,
                type=self._get_menu_type(func)
            )
            menu = ContextMenu(menu_json)
            self._app.add_command(menu, func)
            return menu
        return wrapper

    def add_event(self, callback: CT) -> CT:
        match callback.__name__:
            case 'message' | 'message_delete':
                self._intents += _flags.messages if self._intents & _flags.messages == 0 else 0

        self._listener.add_event(callback.__name__, callback)
        return callback

    def event(self, func: CT) -> CT:
        self.add_event(func)
        return func

    def __iadd__(self, other: Callable[..., Coroutine[Any, Any, Any]]) -> Self:
        self.add_event(other)
        return self

    def remove_event(self, callback_or_name: Callable[..., Coroutine[Any, Any, Any]] | str) -> None:
        name = callback_or_name if isinstance(callback_or_name, str) else callback_or_name.__name__

        match name:
            case 'message' | 'message_delete':
                self._intents -= self._intents & _flags.messages
        self._listener.remove_event(name)

    def __isub__(self, other: Callable[..., Coroutine[Any, Any, Any]] | str) -> Self:
        self.remove_event(other)
        return self
