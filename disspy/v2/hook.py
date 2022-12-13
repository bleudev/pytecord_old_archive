from asyncio import wait as async_wait
from datetime import datetime
from time import mktime, sleep

gateway_version = 10

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
        self._intents = None
        
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

    async def run(self, _session, **options):
        '''
        Run the hook
        '''
        self._intents = options.get('intents', 0)
        self._session = _session

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

            await sleep(interval)

    async def _events(self):
        pass
