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

__all__: tuple = ("DisGuildTemplate", "DisGuild")

from typing import Text, NewType, Union, Optional

import json
from aiohttp import ClientSession
from requests import get


import disspy.user

Json = NewType("Json", dict)

_mainurl = "https://discord.com/api/v10"


class _SendingRestHandler:
    @staticmethod
    async def post(endpoint, __session: ClientSession, _payload=None):
        """post
        POST method

        Args:
            endpoint (str): Url endpoint
            __session (ClientSession): Aiohttp client session
            _payload (dict, optional): Json data. Defaults to None.

        Returns:
            dict: Json output
        """
        _url = _mainurl + endpoint

        if _payload:
            async with __session.post(_url, data=json.dumps(_payload)) as data:
                j = await data.json()

                return j

        else:
            async with __session.post(_url) as data:
                j = await data.json()

                return j

    @staticmethod
    async def patch(endpoint, _payload, __session: ClientSession):
        """patch
        PATCH method

        Args:
            endpoint (str): Url endpoint
            _payload (dict): Json data
            __session (ClientSession): Aiohttp client session

        Returns:
            dict: Json output
        """
        _url = _mainurl + endpoint

        async with __session.patch(_url, data=json.dumps(_payload)) as data:
            j = await data.json()

            return j

    @staticmethod
    async def put(endpoint, __session: ClientSession, _payload=None):
        """put
        PUT method

        Args:
            endpoint (str): Url endpoint
            __session (ClientSession): Aiohttp client session
            _payload (dict, optional): Json data. Defaults to None.

        Returns:
            dict: Json output
        """
        _url = _mainurl + endpoint

        if _payload:
            async with __session.put(_url, data=_payload) as data:
                j = await data.json()

                return j
        else:
            async with __session.put(_url) as data:
                j = await data.json()

                return j

    @staticmethod
    async def delete(endpoint, __session: ClientSession):
        """delete
        DELETE method

        Args:
            endpoint (str): Url endpoint
            __session (ClientSession): Aiohttp client session

        Returns:
            dict: Json output
        """
        _url = _mainurl + endpoint

        async with __session.delete(_url) as data:
            j = await data.json()

            return j

    @staticmethod
    def get(endpoint, hdrs):
        """get
        GET method

        Args:
            endpoint (str): Url endpoint

        Returns:
            dict: Json output
        """
        _url = _mainurl + endpoint

        data = get(_url, headers=hdrs).json()

        return data


class DisGuildTemplate:
    """
    Guild Template for copying channels, roles and other information to other guild
    """

    def __init__(self, data: Json, token: str, __session: ClientSession) -> None:
        self._t: str = str(token)
        self.session = __session

        self.code: str = data["code"]
        self.name = data["name"]
        self.description: Union[str, None] = data["description"]
        self.usage_count: int = int(data["usage_count"])
        self.creator: disspy.user.DisUser = disspy.user.DisUser(
            data["creator"], self._t
        )

        self.guild_id: int = int(data["source_guild_id"])

    async def modify(self, name: Optional[Text], description: Optional[Text] = None):
        """modify()

        Args:
            name (Optional[Text]): New name of template (Optional)
            description (Optional[Text], optional): New description of template (Optional)
        """

        if not name and not description:
            return

        _payload = {"name": name, "description": description}

        if not description:
            del _payload["description"]

        if not name:
            del _payload["name"]

        await _SendingRestHandler.patch(
            f"/guilds/{self.guild_id}/templates/{self.code}", _payload, self.session
        )

        if name:
            self.name = name

        if description:
            self.description = description

    async def delete(self):
        """delete
        Delete template
        """
        await _SendingRestHandler.delete(
            f"/guilds/{self.guild_id}/templates/{self.code}", self.session
        )

    async def sync(self):
        """sync
        Sync template
        """
        await _SendingRestHandler.put(
            f"/guilds/{self.guild_id}/templates/{self.code}", self.session
        )

    async def create_guild(self, name: Text) -> int:
        """create_guild
        Create guild from template

        Args:
            name (Text): Name of guild

        Returns:
            int: Id of created guild from template
        """
        _payload = {"name": name}

        j = await _SendingRestHandler.post(
            f"/guilds/templates/{self.code}", self.session, _payload
        )

        return int(j["id"])


class DisGuild:
    """
    Info
    --------
    Class for manage Guilds in discord
    Atributies
    --------
    :var guild_id: ID of guild

    System atributies
    --------
    :var _t: Token of the bot
    """

    def __init__(self, data: Json, token: Text, __session: ClientSession):
        """
        init object

        :param data: Json data of guild
        :param token: Token of the bot
        """
        self.id = data["id"]
        self._t = token
        self.session = __session

    async def create_template(self, name: Text, description: Text):
        """create_template()

        Args:
            name (Text): Name of template
            description (Text): Description of template
        """
        _payload = {"name": name, "description": description}

        j = await _SendingRestHandler.post(
            f"/guilds/{self.id}/templates", self.session, _payload
        )

        return DisGuildTemplate(j, self._t, self.session)
