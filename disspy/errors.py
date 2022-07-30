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

from typing import Optional

# Constants for messages
missingperms = "Missing permissions!"

# __all__
__all__: tuple = (
    "InternetError",
    "MissingPerms",
    "Unauthorized",
    "BotEventTypeError",
    "BotStatusError",
    "BotEventVisibleError",
    "BotApplicationIdInvalid",
    "ApplicationIdIsNone",
    "InvalidArgument",
    "ClassTypeError",
    "UserNitroTypeError"
)


# Parents for all errors
class DisRunTimeError(RuntimeWarning):
    def __init__(self, code: str, message: str):
        self.__code__ = code
        self.__text__ = message
        self.__message__ = f"{self.__code__} - {self.__text__}"

        super().__init__(self.__message__)


class _DisError(RuntimeError):
    def __init__(self, code: str, message: str):
        self.__code__ = code
        self.__text__ = message
        self.__message__ = f"{self.__code__} - {self.__text__}"

        super().__init__(self.__message__)


# InternetErrors (Will be called when errors code returned)
class InternetError(_DisError):
    def __init__(self, text, code: Optional[str] = None):
        if code is None:
            super().__init__("-1i", text)
        else:
            super().__init__(code, text)


class MissingPerms(DisRunTimeError):
    def __init__(self, text):
        super().__init__("-2i", text)


class Unauthorized(_DisError):
    def __init__(self):
        super().__init__("-3i", "Invalid token!")


# Client errors
class BotEventTypeError(_DisError):
    def __init__(self, text):
        super().__init__("101c", text)


class BotStatusError(_DisError):
    def __init__(self, text):
        super().__init__("102c", text)


class BotEventVisibleError(_DisError):
    def __init__(self, text):
        super().__init__("103c", text)


class BotApplicationIdInvalid(_DisError):
    def __init__(self, text):
        super().__init__("104c", text)


class ApplicationIdIsNone(DisRunTimeError):
    def __init__(self, text):
        super().__init__("105c", text)


class MessageComponentIsBlocked(_DisError):
    def __init__(self, text):
        super().__init__("106c", text)


# Package errors
class InvalidArgument(_DisError):
    def __init__(self, text):
        super().__init__("150p", text)


class ClassTypeError(DisRunTimeError):
    def __init__(self, text):
        super().__init__("151p", text)


# User errors
class UserNitroTypeError(_DisError):
    def __init__(self, text):
        super().__init__("201u", text)
