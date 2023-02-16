from asyncio import run as async_run
from inspect import _empty, getdoc, signature
from typing import Callable, Coroutine, Any

from regex import fullmatch

from disspy_v2.app import AppClient, Command, ContextMenu
from disspy_v2.channel import Channel, Message
from disspy_v2.connection import Connection
from disspy_v2.listener import Listener
from disspy_v2.profiles import User
from disspy_v2.enums import ApplicationCommandOptionType, ApplicationCommandType
from sys import exit as sys_exit

SLASH_COMMAND_VALID_REGEX = r'^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$'

class _flags:
    default = 16
    messages = 55824
    reactions = 9232

class Client:
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

    def _get_options(self, option_tuples: list[tuple[str, tuple[type, Any]]]) -> list[dict]:
        option_jsons = []
        option_types = {
            'SUB_COMMAND': ApplicationCommandOptionType.sub_command,
            'SUB_COMMAND_GROUP': ApplicationCommandOptionType.sub_command_group,
            str: ApplicationCommandOptionType.string,
            int: ApplicationCommandOptionType.integer,
            bool: ApplicationCommandOptionType.boolean,
            User: ApplicationCommandOptionType.user,
            Channel: ApplicationCommandOptionType.channel,
            'ROLE': ApplicationCommandOptionType.role,
            'MENTIONABLE': ApplicationCommandOptionType.mentionable,
            float: ApplicationCommandOptionType.number,
            'ATTACHMENT': ApplicationCommandOptionType.attachment,
        }
        for n, (t, d) in option_tuples:
            option_jsons.append(dict(
                name=n,
                type=option_types[t],
                required=(d == _empty),
            ))
        return option_jsons

    def command(self) -> Callable[..., Command]:
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]) -> Command:
            callable = self._get_callable(func)

            command_json = dict(
                type=ApplicationCommandType.chat_input,
                name=callable.__name__,
            )

            description = getdoc(callable).splitlines()[0]
            params = dict(signature(callable).parameters)
            option_tuples = [(k, (v.annotation, v.default)) for k, v in list(params.items())[1:]]
            option_jsons = self._get_options(x) if (x := option_tuples) else []

            if option_jsons:
                for i in option_jsons:
                    i['description'] = 'No description'

            command_json.update(
                name=callable.__name__,
                description=x if (x := description) else 'No description',
                options=option_jsons,
            )

            if isinstance(func, tuple):
                json, callable, string = func
                if string == 'describe':
                    if command_json.get('options'):
                        for option in command_json.get('options'):
                            for name, description in json.items():
                                if option['name'] == name:
                                    option['description'] = description
                else:
                    for k, v in json.items():
                        command_json[k] = v

            if not self._validate_slash_command(command_json['name']):
                raise ValueError(
                    f'All slash command names must followed {SLASH_COMMAND_VALID_REGEX} regex'
                )

            command = Command(command_json)
            self._app.add_command(command, callable)
            return command
        return wrapper

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

    def event(self, name: str = None) -> Callable[..., None]:
        def wrapper(func) -> None:
            _name = name if name is not None else func.__name__

            if _name in ['message', 'message_delete'] and self._intents & _flags.messages == 0:
                self._intents += _flags.messages
            self._listener.add_event(_name, func)
        return wrapper
