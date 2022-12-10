from typing import Literal
from time import mktime
from asyncio import wait as async_wait
from datetime import datetime

gateway_version = 10

class _Request:
    def __init__(self, data, type_: Literal['send', 'get']) -> None:
        self.data = data
        self.type_ = type_ 

class HookV2:
    def __init__(self, _requester, intents: int) -> None:
        self._requester = _requester
        self.intents = intents
        self.wbsk = None
        self.session = None
        self.listener = None
        self.activity = None
    
    async def send_request(self, data) -> _Request:
        await self.wbsk.send_json(data)
        
        return _Request(data, 'send')
    
    async def get_responce(self):
        try:
            j = await self.wbsk.receive_json()
        except TypeError:
            return
        return _Request(j, 'get')
    
    async def run(self, listener, activity, session):
        self.listener = listener
        self.activity = activity
        self.session = session
        
        await self._runner()
    
    async def _runner(self):
        async with self.session.ws_connect(
            f"wss://gateway.discord.gg/?v={gateway_version}&encoding=json"
        ) as wbsk:
            self.wbsk = wbsk
            
            j = await self.get_responce()
            j = j.data
            
            interval = j['d']['heartbeat_interval']
            
            await self.send_request(
                {
                    "op": 2,
                    "d": {
                        "token": self._requester.token,
                        "intents": self.intents,
                        "properties": {
                            "$os": "linux",
                            "$browser": "disspy",
                            "$device": "disspy",
                        },
                        "presence": {
                            "since": mktime(datetime.now().timetuple()) * 1000,
                            "afk": False,
                            "status": 'online',
                            "activities": [self.activity],
                        },
                    },
                }
            )
            
            await async_wait(
                fs=[
                    self.life(interval / 1000),
                    self.events(),
                ]
            )

    async def life(self, interval):
        pass
    async def events(self):
        pass
