from pytecord.web import BaseWebhook
from asyncio import run as arun

from typing import TYPE_CHECKING, Literal, Callable, Coroutine, Any

if TYPE_CHECKING:
    from pytecord.web import GatewayOutput

class Client:
    def __init__(self, token: str) -> None:
        self.webhook = BaseWebhook(token)
    
    def listen(self, name: Literal['ready']):
        def decorator(func_to_decorate: Callable[..., Coroutine[Any, Any, Any]]):
            match name:
                case 'ready':
                    async def func(data: 'GatewayOutput'):
                        await func_to_decorate()
            
            self.webhook.add_event(name.upper(), func)

        return decorator

    def run(self):
        try:
            arun(self.webhook.run())
        except KeyboardInterrupt:
            exit(0)
