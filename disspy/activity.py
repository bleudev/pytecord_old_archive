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
    "Activity",
    "ActivityType"
)


from typing import (
    NoReturn,
    Dict,
    Any,
    ClassVar
)


class Activity:
    """
    Activity class for changing activities in Discord
    """
    def __init__(self, name: str, activity_type: int) -> NoReturn:
        self.name: str = name
        self.activity_type: int = activity_type

    def json(self) -> Dict[str, Any]:
        """
        json()

        Returns:
            Dict[str, Any]: Json data of activity
        """
        return {
            "name": self.name,
            "type": self.activity_type
        }


class ActivityType:
    """
    Activity types for Activity class

    Attributies: (
        GAME -> Label "Playing in {some_game}"
        STREAMING -> Label "Streaming {some_game}"
        LISTENING -> Label "Listening {some_music}"
        WATCHING -> Label "Watching {some_film}"
        CUSTOM -> Don't Supported
        COMPETING -> Dont't Supported too
    )
    """
    GAME: ClassVar[int] = 0
    STREAMING: ClassVar[int] = 1
    LISTENING: ClassVar[int] = 2
    WATCHING: ClassVar[int] = 3
    CUSTOM: ClassVar[int] = 4
    COMPETING: ClassVar[int] = 5
