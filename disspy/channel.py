from asyncio import get_event_loop

from disspyport utils
from disspyute import Route
from disspyyloads import MessagePayload

class Message:
    def __init__(self, session, **data: MessagePayload) -> None:
        self._session = session
        # Json paramenters
        _ = data.get
        self.id: int = _('id')
        self.channel_id: int = _('channel_id')
        self.author = _('author', None) # todo: Add support for users
        self.content = _('content', None)
        self.timestamp: str = _('timestamp')
        self.edited_timestamp: str | None = _('edited_timestamp', None)
        self.tts: bool = _('tts')
        self.mention_everyone: bool = _('mention_everyone')
        self.mentions: list[dict] = _('mentions', []) # todo: Add support for users
        self.mention_roles: list[dict] = _('mention_roles', []) # todo: Add support for roles
        self.mention_channels: list[dict] = _('mention_channels', []) # todo: Add assign mention channels
        self.attachments: list[dict] = _('attachments', []) # todo: Add support for attachments
        self.embeds: list[dict] = _('embeds', []) # todo: Add support for embeds 
        self.reactions: dict | None = _('reactions', None) # todo: Add support for reactions
        self.pinned: bool = _('pinned')
        self.webhook_id: int | None = _('webhook_id', None)
        self.type: int = _('type')
        self.application_id: int | None = _('application_id', None)
        self.message_reference: data | None = _('message_reference', None) # todo: Add support for message reference
        self.flags: int | None = _('flags', None)
        self.referenced_message: dict | None = _('referenced_message', None) # todo: Add assign referenced message
        self.interaction: dict | None = _('interaction', None) # todo: Add support for interactions
        self.thread: dict | None = _('thread', None) # todo: Add assign thread
        self.components: list[dict] = _('components', [])
        self.stickers: list[dict] = _('stickers', []) # todo: Add support for stickers
        self.position: int | None = _('position', None)

        token = utils.get_token_from_auth(session.headers)
        channel_json  = Route(
            '/channels/%s', self.channel_id,
            method='GET',
            token=token
        ).request()[0]
        self.channel = Channel(session, **channel_json)

    def __str__(self) -> str:
        return self.content

    async def reply(self, content: str):
        payload = {
            'content': content,
            'message_reference': {
                'message_id': self.id
            }
        }
        route = Route(
            '/channels/%s/messages', self.channel_id,
            method='POST',
            payload=payload
        )
        j = await route.async_request(self._session, get_event_loop())
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

        _ = data.get
        self.id: int = _('id')
        self.name: str = _('name')

    def __str__(self) -> str:
        return str(self.name)

    async def send(self, *strings: list[str], sep: str = ' ') -> Message | None:
        payload = {
            'content': str(utils.get_content(*strings, sep=sep))
        }
        route = Route(
            '/channels/%s/messages', self.id,
            method='POST',
            payload=payload
        )
        j = await route.async_request(self._session, get_event_loop())
        return Message(self._session, **j)
