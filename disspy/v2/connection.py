from disspy.v2.hook import Hook
from aiohttp import ClientSession

class Connection:
    def __init__(self, *, token: str, **options) -> None:
        self._run_token = token
        self._hook = Hook(token=token, **options)
        self._headers = {
            "Authorization": f"Bot {token}",
            "content-type": "application/json",
        }
    
    async def run(self, **options):
        async with ClientSession(headers=self._headers) as session:
            await self._hook.run(session, **options)
