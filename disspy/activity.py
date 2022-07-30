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


__all__: tuple = (
    "Activity",
    "ActivityType"
)


from typing import (
    NoReturn,
    Dict,
    Any,
    Optional,
    NewType,
    ClassVar
)

Url = NewType("Url", str)


class Activity:
    """
    Activity class for changing activities in Discord
    """
    def __init__(self, name: str, activity_type: int, url: Optional[Url] = None) -> NoReturn:
        self.name: str = name
        self.activity_type: int = activity_type
        self.url = None
        
        if self.activity_type == 4:  # Custom activity
            raise RuntimeError("Custom activity don't supported!")
        
        if url:
            if self.activity_type == 1:  # Streaming
                self.url = url
            else:
                raise RuntimeError("Url is supported only for streaming status")
            

    def json(self) -> Dict[str, Any]:
        """
        json()

        Returns:
            Dict[str, Any]: Json data of activity
        """
        if self.url:
            return {
                "name": self.name,
                "type": self.activity_type,
                "url": self.url
            }
        else:
            return {
                "name": self.name,
                "type": self.activity_type
            }


class ActivityType:
    """
    Activity types for Activity class

    Attributes: (
        GAME -> Label "Playing {some_game}"
        STREAMING -> Label "Streaming {some_game}"
        LISTENING -> Label "Listening to {name}"
        WATCHING -> Label "Watching {some_film}"
        COMPETING -> Label "Competing in {some_game}"
    """
    GAME: ClassVar[int] = 0
    STREAMING: ClassVar[int] = 1
    LISTENING: ClassVar[int] = 2
    WATCHING: ClassVar[int] = 3
    COMPETING: ClassVar[int] = 5
