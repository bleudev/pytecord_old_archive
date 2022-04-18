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

from disspy.core import RestApiCommands

class ApplicationCommand:
    def __init__(self, name, description, cmd, command_type: int):
        self.name = name
        self.description = description
        self.cmd = cmd
        self.command_type = command_type


class SlashCommand(ApplicationCommand):
    def __init__(self, name, description, cmd):
        super().__init__(name, description, cmd, 1)


class Slash:
    def __init__(self, token, application_id):
        self.token = token
        self.application_id = application_id
        self._rac = RestApiCommands("https://discord.com/api/v10/")

    def _headers(self):
        return {'Authorization': f'Bot {self.token}'}

    def register(self, name, description):
        _payload = {
            "name": name,
            "description": description,
            "type": 1
        }

        return self._rac.POST(f"applications/{self.application_id}/commands", post=_payload, headers=self._headers())

    def getall(self):
        return self._rac.GET(f"applications/{self.application_id}/commands", headers=self._headers())
