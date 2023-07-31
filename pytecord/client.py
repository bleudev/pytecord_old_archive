from pytecord.web import BaseWebhook
from asyncio import run as arun

from typing import TYPE_CHECKING, Literal, Callable, Coroutine, Any

from pytecord.guild import Message, Guild, GuildChannel, MessageDeleteEvent
from pytecord.enums import GatewayIntents

if TYPE_CHECKING:
    from pytecord.web import GatewayOutput

class Client:
    def __init__(self, token: str, debug: bool = False) -> None:
        self.webhook = BaseWebhook(token, debug)
        self.token = token
        self.__intents = GatewayIntents.GUILD_INTEGRATIONS
    
    def listen(self):
        def decorator(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            event_name = func_to_decorate.__name__
            match event_name:
                case 'ready':
                    async def func(data: 'GatewayOutput'):
                        await func_to_decorate()
                case 'message_create' | 'message_update':
                    self.__intents += GatewayIntents.GUILD_MESSAGES
                    self.__intents += GatewayIntents.MESSAGE_CONTENT
                    self.__intents += GatewayIntents.DIRECT_MESSAGES
                    async def func(data: 'GatewayOutput'):
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
