from disspy_v2.mainurl import URL

from requests import get as req_get
from json import dumps

class _MessageSender:
    def __init__(self, session) -> None:
        self.session = session
    
    async def post(self, url, payload):
        async with self.session.post(url, data=dumps(payload)) as response:
            return await response.json()
    def get(self, url, headers):
        return req_get(url, headers=headers).json()

class Message:
    def __init__(self, session, **data) -> None:
        print('DATA:', data['channel_id'])
        self._session = session
        self._sender = _MessageSender(session)
        self.id = data.get('id', None)
        self.content = data.get('content', None)

        channel_id = data['channel_id']
        channel_json = self._sender.get(URL+'/channels/'+channel_id, session.headers)
        print(channel_json)
        self.channel = Channel(session, **channel_json)

class Channel:
    def __init__(self, session, **data) -> None:
        self._session = session
        self._sender = _MessageSender(session)
        self.id = data.get('id', None)

    async def send(self, content, **json) -> Message | None:
        payload = {
            'content': content
        }
        if json:
            for i in json.keys():
                payload.setdefault(i, json[i])
                
        if payload['content']:
            j = await self._sender.post(URL+'/channels/'+self.id+'/messages', payload)
            return Message(self._session, **j)
        return None
