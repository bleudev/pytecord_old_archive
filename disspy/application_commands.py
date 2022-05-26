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
    Type
)


class ApplicationCommand:
    def __init__(self, name, description, cmd, command_type: int):
        self.name = name
        self.description = description
        self.cmd = cmd
        self.command_type = command_type


class SlashCommand(ApplicationCommand):
    def __init__(self, name, description, cmd):
        super().__init__(name, description, cmd, 1)


class Context:
    def __init__(self, interaction_token, interaction_id, bot_token):
        self._interaction_token = interaction_token
        self._interaction_id = interaction_id
        self._headers = {'Authorization': f'Bot {bot_token}'}

    async def send(self, content: str):
        _payload = {
            "type": 4,
            "data": {
                "content": content
            }
        }

        _url = f"https://discord.com/api/v9/interactions/{self._interaction_id}/{self._interaction_token}/callback"

        from requests import post

        post(_url, json=_payload, headers=self._headers)


class Option:
    def __new__(cls, name, description, option_type: int, choices: Optional[list[dict]] = None):
        if choices:
            if Type[option_type] == OptionType.STRING or Type[option_type] == OptionType.INTEGER or Type[option_type] == OptionType.NUMBER:
                return {
                    "name": name,
                    "description": description,
                    "type": option_type,
                    "choices": choices
                }
            else:
                return {
                    "name": name,
                    "description": description,
                    "type": option_type
                }


class OptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11
