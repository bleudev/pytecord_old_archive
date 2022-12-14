from disspy.v2.interfaces import IClient, IApp
from disspy.v2.connection import Connection
from disspy.v2.listener import Listener

from asyncio import run as async_run

class _flags:
    default = 16
    messages = 55824
    reactions = 9232

class ClientV2(IClient, IApp):
    def _resolve_options(self, **options):
        self.debug = options.get('debug', False)

    def __init__(self, *, token: str, **options):
        self.debug = None
        self.token = token
        self._conn = Connection(token=token, **options)
        self._listener = Listener()

        self._resolve_options(**options)

    def run(self, **options):
        async_run(self._conn.run(self._listener, **options))

    def command(self, name=None):
        return

    def context_menu(self, name=None):
        return

    def event(self, name=None):
        def wrapper(func):
            _name = name if name is not None else func.__name__

            self._listener.add_event(_name, func)
        
        return wrapper
