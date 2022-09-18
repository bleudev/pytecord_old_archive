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

from abc import abstractmethod
from typing import (
    Protocol
)


class TypeOf:
    """
    Class for typing in objects receiving in methods

    Example
    def foo(self, bar: TypeOf(foo)):
        ...
    """

    def __new__(cls, *args) -> type:
        """
        :param args: [0] is type
        :param kwargs: No
        :return type:
        """
        return int if str(list(args)[0]).isdigit() else str


class Event:
    """
    Class for event typing

    Ex, Event(DisBotEventType, str)
    """
    def __new__(cls, *args) -> list:
        return list(args)[1]


class SupportsStr(Protocol):
    """SupportsStr
    Protocol with __str__() method
    """
    @abstractmethod
    def __str__(self) -> str:
        pass


# Custom types
Url = str
MISSING = None
