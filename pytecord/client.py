from asyncio import run as arun
from inspect import getdoc, signature, _empty
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Literal

from .commands import AppllicationCommand, AppllicationCommandOption
from .enums import ApplicationCommandType, GatewayIntents
from .guild import Guild, GuildChannel, Message, MessageDeleteEvent
from .user import User
from .utils import get_option_type, rget
from .web import BaseWebhook
from .presence import Presence
from .timer import TimerLoop, At

if TYPE_CHECKING:
    from .web import GatewayOutput

class Client:
    def __init__(self, token: str, debug: bool = False) -> None:
        self.webhook = BaseWebhook(token, debug)
        self.token = token
        self.__timers: list[TimerLoop] = []
        self.__ats: list[At] = []
        self.__intents = GatewayIntents.GUILD_INTEGRATIONS
        self.__presence = None
    
    @property
    def user(self) -> User:
        return self.webhook.get_current_user()
    
    @property
    def guilds(self) -> list[Guild]:
        return self.webhook.get_current_user_guilds()
    
    @property
    def presence(self) -> Presence:
        return self.__presence
    
    @presence.setter
    def presence(self, new: Presence) -> Presence:
        self.__presence = new
        self.__presence.register(self.webhook)
        return self.__presence

    def listen(self):
        def decorator(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            event_name = func_to_decorate.__name__

            if event_name == 'message':
                event_name = 'message_create'

            match event_name:
                case 'ready':
                    async def func(data: 'GatewayOutput'):
                        for i in self.__timers:
                            i.run()
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
    
    def timer(self, *, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
        def wrapper(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            timer = TimerLoop(func_to_decorate, days, hours, minutes, seconds)
            self.__timers.append(timer)
        return wrapper
    
    def at(self, hours: int = 0, minutes: int = 0):
        def wrapper(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            at = At(func_to_decorate, hours, minutes)
            self.__ats.append(at)
        return wrapper
    
    def command(self):
        def wrapper(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            name = func_to_decorate.__name__
            description = getdoc(func_to_decorate).splitlines()[0]
            options = []

            params = dict(signature(func_to_decorate).parameters)
            for op_name, param in list(params.items())[1:]:
                type = get_option_type(param.annotation)
                required = param.default == _empty
                options.append(AppllicationCommandOption(type=type, name=op_name, required=required))


            command = AppllicationCommand(name, description if description else '...', options, ApplicationCommandType.CHAT_INPUT)

            self.webhook.add_command(command, func_to_decorate)
        return wrapper
    
    def get_guild(self, id: int) -> Guild:
        return self.webhook.get_guild(id)
    
    def get_channel(self, id: int) -> GuildChannel:
        return self.webhook.get_channel(id)

    def run(self):
        if not self.webhook.listener.events.get('READY'):
            async def func(data: 'GatewayOutput'):
                for i in self.__timers:
                    i.run()
                await self.webhook.register_app_commands(data)
            self.webhook.add_event('READY', func)
        try:
            self.__presence = Presence([])
            arun(self.webhook.run(self.__intents))
        except KeyboardInterrupt:
            exit(0)
