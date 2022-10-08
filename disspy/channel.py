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

from typing import Optional, Union, List, final, TypedDict

from json import dumps
from aiohttp import ClientSession
from requests import get
from disspy.typ import Url, SupportsStr


from disspy.abstract import Message, Channel
from disspy.embed import DisEmbed
from disspy.guild import DisGuild
from disspy.jsongenerators import _EmbedGenerator
from disspy.ui import ActionRow
from disspy.reaction import DisEmoji, DisOwnReaction
from disspy.payloads import message_payload


__all__: tuple = (
    "DisMessage",
    "DisChannel",
    "DmMessage",
    "DisDmChannel",
    "MessageDeleteEvent",
    "DmMessageDeleteEvent",
)


class MessagePayload(TypedDict):
    """MessagePayload
    Text message payload (typed)
    """

    content: str
    embeds: Optional[list]
    components: Optional[list]


class _SendingRestHandler:
    @staticmethod
    async def execute(
        channel_id: int, payload: MessagePayload, __session: ClientSession
    ) -> dict:
        """execute
        Send messages in channels

        Args:
            channel_id (int): Channel id
            payload (dict): Dict json
            token (str): Bot token

        Returns:
            dict: Json output
        """
        __url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

        async with __session.post(__url, data=dumps(payload)) as data:
            j = await data.json()

            return j

    @staticmethod
    async def put_without_payload(url: Url, __session: ClientSession):
        """put_without_payload
        PUT method wtthout payload

        Args:
            url (Url): url for operation
            token (str): Bot token
        """
        await __session.put(url)

    @staticmethod
    async def delete(url: Url, __session: ClientSession):
        """delete
        DELETE method

        Args:
            url (Url): url for operation
            token (str): Bot token
        """
        await __session.delete(url=url)

    @staticmethod
    async def post_without_payload(url: Url, __session: ClientSession):
        """post_without_payload
        POST method wtthout payload

        Args:
            url (Url): url for operation
            token (str): Bot token
        """
        await __session.post(url=url)

    @staticmethod
    async def create_reaction(endpoint: str, __session: ClientSession):
        """create_reaction()

        Args:
            endpoint (str): Url endpoint
            token (str): Bot token
        """
        url = f"https://discord.com/api/v10{endpoint}"

        await __session.put(url)

    @staticmethod
    async def delete_message(url: Url, __session: ClientSession):
        """delete_message
        Delete message

        Args:
            url (str): Url of message
            token (str): Bot token
        """
        await __session.delete(url=url)


class _GettingChannelData:
    @staticmethod
    def execute(channel_id: int, token: str):
        """execute
        Get channel data by id

        Args:
            channel_id (int): Channel id
            token (str): Bot token

        Returns:
            dict: Json output
        """
        _u = f"https://discord.com/api/v10/channels/{channel_id}"
        _h = {"Authorization": f"Bot {token}"}

        return get(_u, headers=_h).json()

    @staticmethod
    def fetch(channel_id: int, token: str, message_id: int):
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
        _h = {"Authorization": f"Bot {token}"}

        return get(_u, headers=_h).json()


class _GettingGuildData:
    @staticmethod
    def execute(guild_id: int, token: str):
        """execute
        Get guild data

        Args:
            id (int)): Guild id
            token (str): Bot token

        Returns:
            dict: Json output
        """
        _u = f"https://discord.com/api/v10/guilds/{guild_id}"
        _h = {"Authorization": f"Bot {token}"}

        return get(_u, headers=_h).json()


@final
class DisMessage(Message):
    """
    Message in channel
    """

    def __init__(self, _data, __token, __session):
        super().__init__(_data["type"])

        self.json = _data

        self.channel = DisChannel(_data["channel_id"], __token, __session)

        self.content: str = str(_data["content"])

        if _data["embeds"]:
            _j = _data["embeds"]

            self.embeds = []

            for i in _j:
                _e = None

                if i["footer"]["text"]:
                    _e = DisEmbed(
                        title=i["title"],
                        description=i["description"],
                        color=i["color"],
                        footer=i["footer"]["text"]
                    )
                else:
                    _e = DisEmbed(i["title"], description=i["description"], color=i["color"])

                if i["fields"]:
                    for field in i["fields"]:
                        try:
                            _e.add_field(field["name"], field["value"], inline=field["inline"])
                        except KeyError:
                            _e.add_field(field["name"], field["value"])

                self.embeds.append(_e)

        self.id: int = int(_data["id"])

        self._t = __token
        self.session = __session

    async def reply(
        self,
        content: Optional[SupportsStr] = None,
        *,
        embeds: Optional[List[DisEmbed]] = None,
        action_row: Optional[ActionRow] = None
    ):
        """reply
        Reply to message

        Args:
            content (Optional[str], optional): Message content (text). Defaults to None.
            embeds (Optional[List[DisEmbed]], optional): Message embeds (DisEmbed objects).
                                                         Defaults to None.
            action_row (Optional[ActionRow], optional): Action row with components.
                                                         Defaults to None.
        """
        _payload = message_payload(content, embeds, action_row)
        _payload.setdefault("message_reference", {"message_id": self.id})

        if _payload:
            data = await _SendingRestHandler.execute(self.channel.id, _payload, self.session)

            return DisMessage(data, self._t, self.session)

        return None

    async def create_reaction(self, emoji: Union[DisEmoji, str]) -> DisOwnReaction:
        """create_reaction
        Create reaction to message

        Args:
            emoji (Union[DisEmoji, str]): Emoji for reaction

        Returns:
            DisOwnReaction: Your reaction
        """
        if isinstance(emoji, DisEmoji):
            if emoji.type == "custom":
                emoji = f"{emoji.name}:{str(emoji.emoji_id)}"
            elif emoji.type == "normal":
                emoji = emoji.unicode

        await _SendingRestHandler.create_reaction(
            f"/channels/{self.channel.id}/messages/{self.id}/reactions/{emoji}/@me",
            self.session,
        )

        return DisOwnReaction(emoji, self.id, self.channel.id, self._t, self.session)

    async def delete(self):
        """delete
        Delete message
        """
        _u = (
            f"https://discord.com/api/v10/channels/{self.channel.id}/messages/{self.id}"
        )

        await _SendingRestHandler.delete_message(_u, self.session)


@final
class DisChannel(Channel):
    """
    The class for sending messages to discord channels and fetching messages in channels
    """

    def __init__(self, channel_id: int, __token, __session):
        """
        Creating an object DisChannel

        :param id: dict -> id of the channel
        :param rest: Rest -> Rest client with token for channel
        """
        super().__init__()

        self._t = __token
        self.id = channel_id
        self.session = __session

        _data = _GettingChannelData.execute(self.id, self._t)

        try:
            g_id = _data["guild_id"]

            _d = _GettingGuildData.execute(g_id, self._t)

            self.guild = DisGuild(_d, self._t, self.session)
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

    async def send(
        self,
        content: Optional[SupportsStr] = None,
        embeds: Optional[List[DisEmbed]] = None,
        action_row: Optional[ActionRow] = None,
    ) -> Union[DisMessage, None]:
        """send
        Send message in channels

        Examples:
            await channel.send("Test!")  # Send message with content

            await channel.send("Test!", embeds=[DisEmbed()])  # Send message with content and embeds

        Args:
            content (Optional[SupportsStr], optional): Message content. Defaults to None.
            embeds (Optional[List[DisEmbed]], optional): Message embeds (For one embed
                                                         use `[your_embed]`). Defaults to None.
            action_row (Optional[ActionRow], optional): Action row with components.
                                                        Defaults to None.

        Returns:
            DisMessage: Sended message (If message is sended)
            None: If message is not sended
        """
        _payload = message_payload(content, embeds, action_row)

        if _payload:
            data = await _SendingRestHandler.execute(self.id, _payload, self.session)

            return DisMessage(data, self._t, self.session)

        return None

    def fetch(self, message_id: int) -> DisMessage:
        """
        Fetch message
        -----
        :param id: Id of message
        :return DisMessage:
        """
        data = _GettingChannelData.fetch(self.id, self._t, message_id)

        return DisMessage(data, self._t, self.session)

    async def pin(self, message_id: int):
        """pin
        Pin message by id

        Args:
            message_id (int): Message id
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/pins/{message_id}"

        await _SendingRestHandler.put_without_payload(_u, self.session)

    async def unpin(self, message_id: int):
        """unpin
        Unpin message by id

        Args:
            message_id (int): Message id
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/pins/{message_id}"

        await _SendingRestHandler.delete(_u, self.session)

    async def delete(self):
        """delete
        Delete channel
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}"

        await _SendingRestHandler.delete(_u, self.session)

    async def typing(self):
        """typing
        Show typing indicator in channel
        """
        _u = f"https://discord.com/api/v10/channels/{self.id}/typing"

        await _SendingRestHandler.post_without_payload(_u, self.session)


@final
class DmMessage(Message):
    """
    Message in DM channel
    """

    def __init__(self, data, token, session):
        super().__init__(data["type"], True)

        self.json = data
        self._t = token
        self.session = session

        self.id = data["id"]

        self.content = data["content"]
        self.channel = DisDmChannel(data["channel_id"], self._t, session)

    async def reply(
        self,
        content: Optional[SupportsStr] = None,
        embeds: Optional[List[DisEmbed]] = None,
    ):
        """reply
        Reply to message

        Args:
            content (Optional[Any], optional): Message content (text). Defaults to None.
            embeds (Optional[List[DisEmbed]], optional): Message embeds (DisEmbed objects).
                                                         Defaults to None.
        """
        _d = {
            "content": None,
            "embeds": {},
            "message_reference": {"message_id": self.id},
        }

        content = str(content)

        if content:
            _d["content"] = content

        if embeds:
            embeds_jsons = []

            for i in embeds:
                embeds_jsons.append(_EmbedGenerator(i))

            _d["embeds"] = embeds_jsons

        if not embeds and not content:
            return

        await _SendingRestHandler.execute(self.channel.id, _d, self.session)

    async def create_reaction(self, emoji: Union[DisEmoji, str]) -> DisOwnReaction:
        """create_reaction
        Create reaction in message

        Args:
            emoji (Union[DisEmoji, str]): Emoji for reaction

        Returns:
            DisOwnReaction: Your reaction
        """
        if isinstance(emoji, DisEmoji):
            if emoji.type == "custom":
                emoji = f"{emoji.name}:{str(emoji.emoji_id)}"
            elif emoji.type == "normal":
                emoji = emoji.unicode

        await _SendingRestHandler.create_reaction(
            f"/channels/{self.channel.id}/messages/{self.id}/reactions/{emoji}/@me",
            self.session,
        )

        return DisOwnReaction(emoji, self.id, self.channel.id, self._t, self.session)


@final
class DisDmChannel(Channel):
    """
    The class for sending messages to discord DMchannels and fetching messages in DMchannels
    """

    def __init__(self, dm_id: dict, __token, __session):
        """
        Init object
        -----
        :param id: Id of channel
        :param api: DisApi object with token
        """
        super().__init__()

        _data = _GettingChannelData.execute(dm_id, __token)

        self.id = _data["id"]
        self._t = __token
        self.session = __session

    async def send(
        self,
        content: Optional[SupportsStr] = None,
        embeds: Optional[List[DisEmbed]] = None,
        action_row: Optional[ActionRow] = None,
    ) -> Union[DisMessage, None]:
        """
        Sending messages to discord channel

        :param content: str = None -> Content of message which will be sended (default is None)
        :param embeds: List[DisEmbed] = None -> Embeds for message (DisEmbed - embed)
                                                (default is None)
        :param action_row: ActionRow = None -> Action Row with components (default is None)
        :return DisMessage: Message which was sended
        """
        _payload = {"content": None, "embeds": None, "components": None}

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
            data = await _SendingRestHandler.execute(self.id, _payload, self.session)

            return DisMessage(data, self._t, self.session)

        return None

    def fetch(self, message_id: int) -> DisMessage:
        """
        Fetch message
        -----
        :param id: Id of message
        :return DisMessage:
        """
        data = _GettingChannelData.fetch(self.id, self._t, message_id)

        return DisMessage(data, self._t, self.session)


class MessageDeleteEvent:
    """
    MESSAGE_DELETE event class with info about event
    """

    def __init__(self, data: dict, token: str, session):
        self.message_id = data["id"]
        self.channel = DisChannel(data["channel_id"], token, session)


class DmMessageDeleteEvent:
    """
    MESSAGE_DELETE event class with info about event, but in DM channel
    """

    def __init__(self, data: dict, token: str, session):
        self.message_id = data["id"]
        self.channel = DisDmChannel(data["channel_id"], token, session)
