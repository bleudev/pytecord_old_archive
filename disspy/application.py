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
    TypedDict,
    Optional
)

__all__: tuple = (
    "Application",
)

class ApplicationPayload(TypedDict):
    id: int
    name: str
    description: str
    bot_public: bool
    tags: Optional[list]
    custom_install_url: Optional[str]


class Application:
    def __init__(self, payload: ApplicationPayload) -> None:
        self.id = payload['id']
        
        MISSING = "MISSING"

        try:
            self.name = payload['name']
        except KeyError:
            self.name = MISSING

        try:
            self.description = payload['description']
        except KeyError:
            self.description = MISSING

        try:
            self.tags = payload['tags']
        except KeyError:
            self.tags = MISSING

        try:
            self.bot_public = payload['bot_public']
        except KeyError:
            self.bot_public = True

        try:
            self.custom_install_url = payload['custom_install_url']
        except KeyError:
            self.custom_install_url = MISSING
