from asyncio import wait as async_wait
from asyncio import sleep as async_sleep

from datetime import datetime
from time import mktime

from disspy_v2.listener import Listener
from disspy_v2.channel import Message, RawMessage

gateway_version = 10

class _Gateway_Event:
    def __init__(self, **_dict) -> None:
        self.op = _dict.get('op', 0)
        self.data = _dict.get('d', {})
        self.session = _dict.get('s', 0)
        self.type = _dict.get('t', 'NONE')


class Hook:
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
        self._listener = None
        self._user_id = None

    async def _get(self) -> dict:
        try:
            j = await self._ws.receive_json()
        except TypeError:
            return
        return j

    async def _send(self, data: dict) -> dict:
        await self._ws.send_json(data)
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

    async def run(self, _session, listener: Listener, **options):
        '''
        Run the hook
        '''
        self._intents = options.get('intents', 0)
        self._session = _session
        self._listener = listener

        async with self._session.ws_connect(
            f"wss://gateway.discord.gg/?v={gateway_version}&encoding=json"
        ) as _ws:
            self._ws = _ws

            data = await self._get()
            interval = data["d"]["heartbeat_interval"] / 1000

            await self._identify()

            await async_wait(
                fs=[
                    self._life(interval),
                    self._events(),
                ]
            )

    async def _life(self, interval):
        while True:
            j = {"op": 1, "d": None, "t": None}
            await self._send(j)

            print('Sending heartbeat:', j)

            await async_sleep(interval)

    async def _events(self):
        while True:
            _data = await self._get()
            event = _Gateway_Event(**_data)
            print(_data)

            if event.type == 'READY':
                self._user_id = event.data['user']['id']

                await self._listener.invoke_event('ready')
            if event.type in ['MESSAGE_CREATE', 'MESSAGE_UPDATE']:
                message_data = event.data

                if message_data['author']['id'] != self._user_id:
                    message = Message(self._session, **message_data)
                    await self._listener.invoke_event('message', message)
            if event.type == 'MESSAGE_DELETE':
                raw_message = RawMessage(self._session, **event.data)
                await self._listener.invoke_event('message_delete', raw_message)
