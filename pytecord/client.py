from asyncio import run as arun
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Literal
from inspect import getdoc

from .commands import ApllicationCommand
from .enums import GatewayIntents
from .guild import Guild, GuildChannel, Message, MessageDeleteEvent
from .user import User
from .web import BaseWebhook

if TYPE_CHECKING:
    from .web import GatewayOutput

class Client:
    def __init__(self, token: str, debug: bool = False) -> None:
        self.webhook = BaseWebhook(token, debug)
        self.token = token
        self.__intents = GatewayIntents.GUILD_INTEGRATIONS
        self.__user_id = None
    
    @property
    def user(self) -> User:
        return User(self.webhook.get_user(self.__user_id), self.token)
    
    def listen(self):
        def decorator(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            event_name = func_to_decorate.__name__
            match event_name:
                case 'ready':
                    async def func(data: 'GatewayOutput'):
                        self.__user_id = data.d['user']['id']
                        await self.webhook.register_app_commands(data)
                        await func_to_decorate()
                case 'message_create' | 'message_update':
                    self.__intents += GatewayIntents.GUILD_MESSAGES
                    self.__intents += GatewayIntents.MESSAGE_CONTENT
                    self.__intents += GatewayIntents.DIRECT_MESSAGES
                    async def func(data: 'GatewayOutput'):
                        if not data.d['author'].get('bot', False):
                            message = Message(data.d, self.token)
                            await func_to_decorate(message)
                case 'message_delete':
                    self.__intents += GatewayIntents.GUILD_MESSAGES
                    self.__intents += GatewayIntents.DIRECT_MESSAGES
                    async def func(data: 'GatewayOutput'):
                        event = MessageDeleteEvent(data.d, self.token)
                        await func_to_decorate(event)
                case _:
                    raise ValueError('Invalid event name: %s' % event_name)
            
            self.webhook.add_event(event_name.upper(), func)

        return decorator
    
    def command(self):
        def wrapper(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            name = func_to_decorate.__name__
            description = getdoc(func_to_decorate).splitlines()[0]

            command = ApllicationCommand(name, description if description else '...')

            self.webhook.add_command(command, func_to_decorate)
        return wrapper
    
    def get_guild(self, id: int) -> Guild:
        return self.webhook.get_guild(id)
    
    def get_channel(self, id: int) -> GuildChannel:
        return self.webhook.get_channel(id)

    def run(self):
        if not self.webhook.listener.events.get('READY'):
            async def func(data: 'GatewayOutput'):
                self.__user_id = data.d['user']['id']
                await self.webhook.register_app_commands(data)
            self.webhook.add_event('READY', func)
        try:
            arun(self.webhook.run(self.__intents))
        except KeyboardInterrupt:
            exit(0)
