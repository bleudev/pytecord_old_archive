from .web import BaseWebhook
from asyncio import run as arun

from typing import TYPE_CHECKING, Literal, Callable, Coroutine, Any

from .guild import Message, Guild, GuildChannel, MessageDeleteEvent
from .enums import GatewayIntents
from .user import User

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
    
    def get_guild(self, id: int) -> Guild:
        return self.webhook.get_guild(id)
    
    def get_channel(self, id: int) -> GuildChannel:
        return self.webhook.get_channel(id)

    def run(self):
        try:
            arun(self.webhook.run(self.__intents))
        except KeyboardInterrupt:
            exit(0)
