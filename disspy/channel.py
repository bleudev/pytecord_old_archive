"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import (
    Optional,
    Union,
    List,
    NoReturn
)

from json import dumps
from aiohttp import ClientSession
from requests import get
from disspy.typ import Url


from disspy.embed import DisEmbed
from disspy.message import DisMessage
from disspy.guild import DisGuild
from disspy.jsongenerators import _EmbedGenerator
from disspy.ui import ActionRow

__all__: tuple = (
    "DisChannel",
    "DisDmChannel"
)


class _SendingRestHandler:
    @staticmethod
    async def execute(channel_id: int, payload: dict, token: str) -> dict:
        """execute
        Send messages in channels

        Args:
            channel_id (int): Channel id
            payload (dict): Dict json
            token (str): Bot token

        Returns:
            dict: Json output
        """
        async with ClientSession(headers={'Authorization': f'Bot {token}',
                                          'content-type': 'application/json'}) as session:
            _u = f"https://discord.com/api/v9/channels/{channel_id}/messages"

            async with session.post(_u, data=dumps(payload)) as data:
                j = await data.json()

                return j

    @staticmethod
    async def put_without_payload(url: Url, token):
        """put_without_payload
        PUT method wtthout payload

        Args:
            url (Url): url for operation
            token (str): Bot token
        """
        async with ClientSession(headers={'Authorization': f'Bot {token}',
                                          'content-type': 'application/json'}) as session:
            await session.put(url)

    @staticmethod
    async def delete(url: Url, token: str):
        """delete
        DELETE method

        Args:
            url (Url): url for operation
            token (str): Bot token
        """
        async with ClientSession(headers={'Authorization': f'Bot {token}',
                                          'content-type': 'application/json'}) as session:
            await session.delete(url=url)

    @staticmethod
    async def post_without_payload(url: Url, token: str):
        """post_without_payload
        POST method wtthout payload

        Args:
            url (Url): url for operation
            token (str): Bot token
        """
        async with ClientSession(headers={'Authorization': f'Bot {token}',
                                          'content-type': 'application/json'}) as session:
            await session.post(url=url)


class _GettingChannelData:
    @staticmethod
    def execute(channel_id, token):
        """execute
        Get channel data by id

        Args:
            channel_id (int): Channel id
            token (str): Bot token

        Returns:
            dict: Json output
        """
        _u = f"https://discord.com/api/v10/channels/{channel_id}"
        _h = {'Authorization': f'Bot {token}'}

        return get(_u, headers=_h).json()

    @staticmethod
    def fetch(channel_id, token, message_id):
        """fetch
        Fetch message by channel id and message id

        Args:
            channel_id (int): Channel id
            token (str): Bot token
            message_id (int): Message id

        Returns:
            dict: Json output
        """
        _u = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"
        _h = {'Authorization': f'Bot {token}'}

        return get(_u, headers=_h).json()


class _GettingGuildData:
    @staticmethod
    def execute(guild_id, token):
        """execute
        Get guild data

        Args:
            id (int)): Guild id
            token (str): Bot token

        Returns:
            dict: Json output
        """
        _u = f"https://discord.com/api/v10/guilds/{guild_id}"
        _h = {'Authorization': f'Bot {token}'}

        return get(_u, headers=_h).json()


class _ShowonlyContext:
    def __init__(self, message: DisMessage, token: str, channel_id: int) -> NoReturn:
        self._t = token
        self._channel_id = int(channel_id)

        self._content = message.content

        self._embeds = message.embeds

    async def _send(self, payload) -> DisMessage:
        data = await _SendingRestHandler.execute(self._channel_id, payload, self._t)

        return DisMessage(data, self._t)

    async def content(self) -> DisMessage:
        """content
        Send only content

        Returns:
            DisMessage: Showed message
        """
        _payload = {
            "content": self._content
        }

        _m = await self._send(_payload)

        return _m

    async def embeds(self) -> DisMessage:
        """embeds
        Send only embeds

        Returns:
            DisMessage: Showed message
        """
        _payload = {
            "embeds": self._embeds
        }

        _m = await self._send(_payload)

        return _m

class DisChannel:
    """
    The class for sending messages to discord channels and fetching messages in channels
    """
    def __init__(self, channel_id: int, _token):
        """
        Creating an object DisChannel

        :param id: dict -> id of the channel
        :param rest: Rest -> Rest client with token for channel
        """
        self._t = _token
        self.id = channel_id

        _data = _GettingChannelData.execute(self.id, self._t)

        try:
            g_id = _data["guild_id"]

            _d = _GettingGuildData.execute(g_id, self._t)

            self.guild = DisGuild(_d, self._t)
        except KeyError:
            pass

    def __eq__(self, other):
        """
        __eq__ have using in "==" operator

        :param other: Other object (DisChannel)
        :return: bool -> if id of this object equals with id of other object
                         :returns: True, else False:
        """
        return self.id == other.id

    async def send(self, content: Optional[str] = None, embeds: Optional[List[DisEmbed]] = None,
                   action_row: Optional[ActionRow] = None) -> Union[DisMessage, None]:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embeds: List[DisEmbed] = None -> Embeds for message (DisEmbed - embed)
                                                (default is None)
        :param action_row: ActionRow = None -> Action Row with components (default is None)
        :return DisMessage: Message which was sended
        """
        _payload = {
            "content": None,
            "embeds": None,
            "components": None
        }

        if embeds:
            embeds_json = []

            for i in embeds:
                embeds_json.append(_EmbedGenerator(i))

            _payload["embeds"] = embeds_json
        else:
            del _payload["embeds"]

        if content:
            _payload["content"] = content
        else:
            del _payload["content"]

        if action_row:
            if action_row.json["components"]:
                _payload["components"] = action_row.json
            else:
                del _payload["components"]

        if _payload:
            data = await _SendingRestHandler.execute(self.id, _payload, self._t)

            return DisMessage(data, self._t)
        else:
            return None

    async def show(self, message: DisMessage):
        """show
        Send all info about message in channel

        Args:
            message (DisMessage): Message for showing

        Returns:
            DisMessage: Showed message
        """
        json_data = {}

        if message.content:
            json_data.setdefault("content", message.content)

        if message.embeds:
            json_data.setdefault("embeds", message.embeds)

        data = await _SendingRestHandler.execute(self.id, json_data, self._t)

        return DisMessage(data, self._t)

    def showonly(self, message: DisMessage) -> _ShowonlyContext:
        """showonly
        show() method, but send only embeds or content

        Args:
            message (DisMessage): Message for showing

        Returns:
            _ShowonlyContext: Context for showing
        """
        return _ShowonlyContext(message, self._t, self.id)

    def fetch(self, message_id: int) -> DisMessage:
        """
        Fetch message
        -----
        :param id: Id of message
        :return DisMessage:
        """
        data = _GettingChannelData.fetch(self.id, self._t, message_id)

        return DisMessage(data, self._t)

    async def pin(self, message_id: int):
        """pin
        Pin message by id

        Args:
            message_id (int): Message id
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/pins/{message_id}"

        await _SendingRestHandler.put_without_payload(_u, self._t)

    async def unpin(self, message_id: int):
        """unpin
        Unpin message by id

        Args:
            message_id (int): Message id
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/pins/{message_id}"

        await _SendingRestHandler.delete(_u, self._t)

    async def delete(self):
        """delete
        Delete channel
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}"

        await _SendingRestHandler.delete(_u, self._t)

    async def typing(self):
        """typing
        Show typing indicator in channel
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/typing"

        await _SendingRestHandler.post_without_payload(_u, self._t)


class DisDmChannel:
    """
    The class for sending messages to discord DMchannels and fetching messages in DMchannels
    """
    def __init__(self, dm_id: dict, token):
        """
        Init object
        -----
        :param id: Id of channel
        :param api: DisApi object with token
        """
        _data = _GettingChannelData.execute(dm_id, token)

        self.id = _data["id"]
        self._t = token

    async def send(self, content: Optional[str] = None, embeds: Optional[List[DisEmbed]] = None,
                   action_row: Optional[ActionRow] = None) -> Union[DisMessage, None]:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embeds: List[DisEmbed] = None -> Embeds for message (DisEmbed - embed)
                                                (default is None)
        :param action_row: ActionRow = None -> Action Row with components (default is None)
        :return DisMessage: Message which was sended
        """
        _payload = {
            "content": None,
            "embeds": None,
            "components": None
        }

        if embeds:
            embeds_json = []

            for i in embeds:
                embeds_json.append(_EmbedGenerator(i))

            _payload["embeds"] = embeds_json
        else:
            del _payload["embeds"]

        if content:
            _payload["content"] = content
        else:
            del _payload["content"]

        if action_row:
            if action_row.json["components"]:
                _payload["components"] = action_row.json
            else:
                del _payload["components"]

        if _payload:
            data = await _SendingRestHandler.execute(self.id, _payload, self._t)

            return DisMessage(data, self._t)
        else:
            return None

    def fetch(self, message_id: int) -> DisMessage:
        """
        Fetch message
        -----
        :param id: Id of message
        :return DisMessage:
        """
        data = _GettingChannelData.fetch(self.id, self._t, message_id)

        return DisMessage(data, self._t)
