from asyncio import get_event_loop
from typing import TYPE_CHECKING

from pytecord import utils
from pytecord.payloads import MessagePayload
from pytecord.route import Route

if TYPE_CHECKING:
    from pytecord.annotations import Strable

__all__ = (
    'Message',
    'RawMessage',
    'Channel',
)

class Message:
    '''
    Channel message object
    
    ### Magic operations
    ---

    `str()` -> Message content

    `int()` -> Message id

    `in` -> Check what message contains in channel
    
    `==` -> This message is equal with other message

    `!=` -> This message is not equals with other message

    `<` -> Message life time (how long the message has been sent) less that other message life time
    (ID1 > ID2)

    `>` -> Message life time more that other message life time (ID1 < ID2)

    `<=` -> Message life time less or equals that other message life time (ID1 >= ID2)

    `>=` -> Message life time more or equals that other message life time (ID1 <= ID2)
    ```
    # message1.id = 1; message2.id = 2; message = message1
    str(message) # message.content
    int(message) # message.id
    
    if message in channel: # if message.channel.id == channel.id
        print('This message in this channel!')

    print('Equals!' if message1 == message2 else 'Not equals!')
    print('Not equals!' if message1 != message2 else 'Equals!')
    
    print(message1 < message2) # False
    print(message1 > message2) # True
    print(message1 <= message2) # False
    print(message1 >= message2) # True
    ```
    '''
    def __init__(self, session, **data: MessagePayload) -> None:
        self._session = session

        _ = data.get
        self.id: int = int(_('id'))
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
    
    @property
    def channel(self) -> 'Channel':
        channel_json, _  = Route(
            '/channels/%s', self.channel_id,
            method='GET',
            token=utils.get_token_from_auth(self._session.headers)
        ).request()
        return Channel(self._session, **channel_json)

    def __str__(self) -> str:
        return self.content
    def __int__(self) -> int:
        return self.id
    def __eq__(self, __o: 'Message') -> bool: # ==
        return self.id == __o.id
    def __ne__(self, __o: 'Message') -> bool: # !=
        return self.id != __o.id
    def __lt__(self, other: 'Message') -> bool: # <
        return self.id > other.id
    def __gt__(self, other: 'Message') -> bool: # >
        return self.id < other.id
    def __le__(self, other: 'Message'): # <=
        return self.id >= other.id
    def __ge__(self, other: 'Message'): # >=
        return self.id <= other.id

    async def reply(self, *strings: 'list[Strable]', sep: str = ' '):
        '''
        Reply to a message
        '''
        payload = utils.message_payload(*strings, sep=sep)
        payload['message_reference'] = {
            'message_id': self.id
        }

        route = Route(
            '/channels/%s/messages', self.channel_id,
            method='POST',
            payload=payload
        )
        j, _ = await route.async_request(self._session, get_event_loop())
        return Message(self._session, **j)


class RawMessage:
    def __init__(self, session, **data) -> None:
        self._session = session

        self.id: int = data.get('id', None)
        self.channel_id: int = data.get('channel_id', None)
        self.guild_id: int | None = data.get('guild_id', None)


class Channel:
    '''
    Channel object.

    ### Magic operations
    ---

    `str()` -> Name of channel

    `int()` -> Channel id
    
    `in` -> Check what message contains in channel

    `[key]` -> Fetch the message
    ```
    str(channel)
    int(channel)

    if message in channel:
        print('This message in this channel!')

    fetched_message = channel[1076055795042615298]
    ```
    '''
    def __init__(self, session, **data) -> None:
        self._session = session

        _ = data.get
        self.id: int = int(_('id'))
        self.name: str = _('name')

    def fetch(self, message_to_fetch_id: int) -> 'Message':
        data, _ = Route(
            '/channels/%s/messages/%s', self.id, str(message_to_fetch_id),
            method='GET',
            token=utils.get_token_from_auth(self._session.headers)
        ).request()
        return Message(self._session, **data)

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id

    def __contains__(self, value: 'Message') -> bool:
        return self.id == value.channel_id

    def __getitem__(self, key: int) -> 'Message':
        return self.fetch(key)

    async def send(self, *strings: 'list[Strable]', sep: str = ' ', tts: bool = False) -> 'Message | None':
        route = Route(
            '/channels/%s/messages', self.id,
            method='POST',
            payload=utils.message_payload(*strings, sep=sep, tts=tts)
        )
        j, _ = await route.async_request(self._session, get_event_loop())
        return Message(self._session, **j)
