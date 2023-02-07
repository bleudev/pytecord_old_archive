from typing import Optional, Literal, Iterable, TYPE_CHECKING
from disspy_v2 import utils

from requests import get as GET
from requests import post as POST
from requests import put as PUT
from requests import delete as DELETE
from requests import patch as PATCH
from requests import options as OPTIONS
from requests import head as HEAD
from requests.exceptions import JSONDecodeError
from asyncio import gather

if TYPE_CHECKING:
    from requests import Response
    from aiohttp import ClientSession, ClientResponse
    from asyncio import AbstractEventLoop

API_VERSION = 10
BASE = f'https://discord.com/api/v{API_VERSION}'

class Route:
    def __init__(
        self,
        endpoint: Optional[str] = '',
        *params: Iterable[str],
        method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'] = 'GET',
        token: Optional[str] = '',
        payload: Optional[dict] = {}
    ) -> None:
        self.endpoint = endpoint % params
        self.url = BASE + self.endpoint
        self.method = method
        self.hdrs = utils.auth(token)
        self.data = payload

    def request(self):
        funcs = {
            'GET': GET,
            'POST': POST,
            'PUT': PUT,
            'DELETE': DELETE,
            'PATCH': PATCH,
            'OPTIONS': OPTIONS,
            'HEAD': HEAD,
        }
        func = funcs[self.method]

        resp: 'Response' = func(
            url=self.url,
            json=self.data,
            headers=self.hdrs,
            timeout=2,
        )

        try:
            J = resp.json()
        except JSONDecodeError:
            J = resp.text
        C = resp.status_code
        return J, C

    async def _async_request_task(self, session: 'ClientSession'):
        funcs = {
            'GET': session.get,
            'POST': session.post,
            'PUT': session.put,
            'DELETE': session.delete,
            'PATCH': session.patch,
            'OPTIONS': session.options,
            'HEAD': session.head,
        }
        func = funcs[self.method]

        async with func(
            url=self.url,
            json=self.data,
            headers=self.hdrs,
            timeout=2,
        ) as r:
            r: 'ClientResponse' = r
            return await r.json()


    async def async_request(self, session: 'ClientSession', loop: 'AbstractEventLoop'):
        tasks = [loop.create_task(self._async_request_task(session))]
        await gather(*tasks)
