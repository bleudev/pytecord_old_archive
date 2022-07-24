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

__all__: tuple[str] = (
    "DisGuildTemplate",
    "DisGuild"
)

from email import header
from aiohttp import ClientSession
from requests import get
from typing import (
    Text,
    NewType,
    Union,
    Optional
)

import disspy.user
import json

Json = NewType("Json", dict)

class _SendingRestHandler:
    _mainurl = "https://discord.com/api/v10"
    
    def __init__(self, token: str):
        self.hdrs = {'Authorization': f'Bot {token}', "content-type": "application/json"}
        
    def _gen_url(self, endpoint) -> str:
        return self._mainurl + endpoint
    
    async def post(self, endpoint, _payload=None):
        if _payload:
            async with ClientSession(headers=self.hdrs) as s:
                async with s.post(self._gen_url(endpoint), data=json.dumps(_payload)) as d:
                    j = await d.json()
                    
                    return j
        
        else:
            async with ClientSession(headers=self.hdrs) as s:
                async with s.post(self._gen_url(endpoint)) as d:
                    j = await d.json()
                    
                    return j
        
    async def patch(self, endpoint, _payload):
        async with ClientSession(headers=self.hdrs) as s:
            async with s.patch(self._gen_url(endpoint), data=json.dumps(_payload)) as d:
                j = await d.json()
                    
                return j
    
    async def put(self, endpoint, _payload=None):
        if _payload:
            async with ClientSession(headers=self.hdrs) as s:
                async with s.post(self._gen_url(endpoint), data=_payload) as d:
                    j = await d.json()
                    
                    return j
        else:
            async with ClientSession(headers=self.hdrs) as s:
                async with s.put(self._gen_url(endpoint)) as d:
                    j = await d.json()
                        
                    return j
    
    async def delete(self, endpoint):
        async with ClientSession(headers=self.hdrs) as s:
            async with s.delete(self._gen_url(endpoint)) as d:
                j = await d.json()

                return j
    
    def get(self, endpoint):
        data = get(self._gen_url(endpoint), headers=self.hdrs).json()
        
        return data
    
    
class DisGuildTemplate:
    def __init__(self, data: Json, token: str) -> None:
        self._t: str = str(token)
        
        self.code: str = data["code"]
        self.name = data["name"]
        self.description: Union[str, None] = data["description"]
        self.usage_count: int = int(data["usage_count"])
        self.creator: disspy.user.DisUser = disspy.user.DisUser(data["creator"], self._t)
        
        self.guild_id: int = int(data["source_guild_id"])
        
    async def modify(self, name: Optional[Text], description: Optional[Text] = None):
        """modify()

        Args:
            name (Optional[Text]): New name of template (Optional)
            description (Optional[Text], optional): New description of template (Optional)
        """
        
        if not name and not description:
            return
        
        _payload = {
            "name": name,
            "description": description
        }
        
        if not description:
            del _payload["description"]
        
        if not name:
            del _payload["name"]
            
        j = await _SendingRestHandler(self._t).patch(f"/guilds/{self.guild_id}/templates/{self.code}", _payload)

        if name:
            self.name = name
            
        if description:
            self.description = description
            
    async def delete(self):
        j =await _SendingRestHandler(self._t).delete(f"/guilds/{self.guild_id}/templates/{self.code}")
        
    async def sync(self):
        await _SendingRestHandler(self._t).put(f"/guilds/{self.guild_id}/templates/{self.code}")
    
    async def create_guild(self, name: Text):
        _payload = {
            "name": name
        }
        
        j = await _SendingRestHandler(self._t).post(f"/guilds/templates/{self.code}", _payload)
        
        return DisGuild(j, self._t)
        


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
    def __init__(self, data: Json, token: Text):
        """
        init object

        :param data: Json data of guild
        :param token: Token of the bot
        """
        self.id = data["id"]
        self._t = token
        
    async def create_template(self, name: Text, description: Text):
        """create_template()

        Args:
            name (Text): Name of template
            description (Text): Description of template
        """
        _payload = {
            "name": name,
            "description": description
        }
                
        j = await _SendingRestHandler(self._t).post(f"/guilds/{self.id}/templates", _payload)
        
        return DisGuildTemplate(j, self._t)
