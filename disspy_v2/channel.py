from disspy_v2.mainurl import URL
from disspy_v2 import utils

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
        self._session = session
        self._sender = _MessageSender(session)
        
        # Json paramenters
        self.id: int = data.get('id')
        self.channel_id: int = data.get('channel_id')
        self.author = data.get('author', None) # todo: Add support for users
        self.content = data.get('content', None)
        self.timestamp: str = data.get('timestamp')
        self.edited_timestamp: str | None = data.get('edited_timestamp', None)
        self.tts: bool = data.get('tts')
        self.mention_everyone: bool = data.get('mention_everyone')
        self.mentions: list[dict] = data.get('mentions', []) # todo: Add support for users
        self.mention_roles: list[dict] = data.get('mention_roles', []) # todo: Add support for roles
        self.mention_channels: list[dict] = data.get('mention_channels', []) # todo: Add assign mention channels
        self.attachments: list[dict] = data.get('attachments', []) # todo: Add support for attachments
        self.embeds: list[dict] = data.get('embeds', []) # todo: Add support for embeds 
        self.reactions: dict | None = data.get('reactions', None) # todo: Add support for reactions
        self.pinned: bool = data.get('pinned')
        self.webhook_id: int | None = data.get('webhook_id', None)
        self.type: int = data.get('type')
        self.application_id: int | None = data.get('application_id', None)
        self.message_reference: data | None = data.get('message_reference', None) # todo: Add support for message reference
        self.flags: int | None = data.get('flags', None)
        self.referenced_message: dict | None = data.get('referenced_message', None) # todo: Add assign referenced message
        self.interaction: dict | None = data.get('interaction', None) # todo: Add support for interactions
        self.thread: dict | None = data.get('thread', None) # todo: Add assign thread
        self.components: list[dict] = data.get('components', [])
        self.stickers: list[dict] = data.get('stickers', []) # todo: Add support for stickers
        self.position: int | None = data.get('position', None)

        channel_json = self._sender.get(URL+'/channels/'+self.channel_id, session.headers)
        self.channel = Channel(session, **channel_json)

    async def reply(self, content: str):
        payload = {
            'content': content,
            'message_reference': {
                'message_id': self.id
            }
        }
        j = await self._sender.post(URL+'/channels/'+self.channel_id+'/messages', payload)
        return Message(self._session, **j)


class RawMessage:
    def __init__(self, session, **data) -> None:
        self._session = session

        self.id: int = data.get('id', None)
        self.channel_id: int = data.get('channel_id', None)
        self.guild_id: int | None = data.get('guild_id', None)


class Channel:
    def __init__(self, session, **data) -> None:
        self._session = session
        self._sender = _MessageSender(session)
        
        _ = data.get
        self.id: int = _('id')
        self.name: str = _('name')

    def __str__(self) -> str:
        return str(self.name)

    async def send(self, *strings: list[str], sep: str = ' ') -> Message | None:
        payload = {
            'content': str(utils.get_content(*strings, sep=sep))
        }
        j = await self._sender.post(URL+'/channels/'+self.id+'/messages', payload)
        return Message(self._session, **j)
