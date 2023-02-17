from asyncio import run as async_run
from inspect import _empty, getdoc, signature
from sys import exit as sys_exit
from typing import Any, Callable, Coroutine, Self, TypeVar

from regex import fullmatch

from disspy.app import AppClient, Command, ContextMenu
from disspy.channel import Channel, Message
from disspy.connection import Connection
from disspy.enums import ApplicationCommandOptionType, ApplicationCommandType
from disspy.listener import Listener
from disspy.profiles import User

SLASH_COMMAND_VALID_REGEX = r'^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$'

CT = TypeVar( 'CT', bound=Callable[..., Coroutine[Any, Any, Any]] ) 

class _flags:
    default = 16
    messages = 55824
    reactions = 9232

class Client:
    '''
    Discord client.
    
    ### Magic operations
    
    += -> Add the event to the client
    
    ```
    async def ready(): ...
    client += ready
    ```

    -= -> Remove the event from the client
    
    ```
    @client.event
    async def ready(): ...
    client -= ready # or 'ready'
    ```

    Calling -> Run the bot
    
    ```
    client() # equals to client.run()
    ```

    repr() -> Get client data (for example, commands)
    
    ```
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
            User: ApplicationCommandOptionType.user,
            Channel: ApplicationCommandOptionType.channel,
            'ROLE': ApplicationCommandOptionType.role,
            'MENTIONABLE': ApplicationCommandOptionType.mentionable,
            float: ApplicationCommandOptionType.number,
            'ATTACHMENT': ApplicationCommandOptionType.attachment,
        }
        for n, (t, d) in option_tuples: # pylint: disable=invalid-name
            option_jsons.append({
                'name': n,
                'type': option_types[t],
                'required': d == _empty,
            })
        return option_jsons

    def command(self) -> Callable[..., Command]:
        """
        Create an `app command`
        
        ```
        @client.command()
        @app.describe(
            first='First argument'
        )
        async def test(ctx: Context, first: str):
            await ctx.send_message(first)
        ```

        Returns:
            Callable[..., Command]: Wrapper
        """
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]) -> Command:
            callable = self._get_callable(func)

            command_json = {
                'type': ApplicationCommandType.chat_input,
                'name': callable.__name__,
            }

            description = x.splitlines()[0] if (x := getdoc(callable)) else None # pylint: disable=invalid-name

            params = dict(signature(callable).parameters)
            option_tuples = [(k, (v.annotation, v.default)) for k, v in list(params.items())[1:]]
            option_jsons = self._get_options(x) if (x := option_tuples) else [] # pylint: disable=invalid-name

            if option_jsons:
                for i in option_jsons:
                    i['description'] = 'No description'

            command_json.update(
                name=callable.__name__,
                description=x if (x := description) else 'No description', # pylint: disable=invalid-name
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
                    for k, v in json.items(): # pylint: disable=invalid-name
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

    def add_event(self, callback: Callable[..., Coroutine[Any, Any, Any]]) -> None:
        match callback.__name__:
            case 'message' | 'message_delete':
                self._intents += _flags.messages if self._intents & _flags.messages == 0 else 0

        self._listener.add_event(callback.__name__, callback)

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
