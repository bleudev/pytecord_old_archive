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
MISSINGPERMS = "Missing permissions!"

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
    "MessageComponentIsBlocked",
    "InvalidArgument",
    "ClassTypeError",
    "UserNitroTypeError",
    "JsonError",
    "ActivityUrlError",
)


# Parents for all errors
class DisError(Exception):
    """DisRunTimeError
    Parent for other classes
    """

    def __init__(self, code: str, message: str):
        self.__code__ = code
        self.__text__ = message
        self.__message__ = f"{self.__text__} (Error code: {self.__code__})"

        super().__init__(self.__message__)


# InternetErrors (Will be called when errors code returned)
class InternetError(DisError):
    """InternetError
    Error with internet (For example, with Wi-Fi)
    """

    def __init__(self, text, code: Optional[str] = None):
        if code is None:
            super().__init__("-1i", text)
        else:
            super().__init__(code, text)


class MissingPerms(DisError):
    """MissingPerms
    Missing permissions in Discord
    """

    def __init__(self, text):
        super().__init__("-2i", text)


class Unauthorized(DisError):
    """Unauthorized
    Invalid token!
    """

    def __init__(self):
        super().__init__("-3i", "Invalid token!")


# Client errors
class BotEventTypeError(DisError):
    """BotEventTypeError
    Invalid bot event type
    """

    def __init__(self, text):
        super().__init__("101c", text)


class BotStatusError(DisError):
    """BotStatusError
    Invalid bot status
    """

    def __init__(self, text):
        super().__init__("102c", text)


class BotEventVisibleError(DisError):
    """BotEventVisibleError
    Bot don't can see this event (because bot intents < need intents)
    """

    def __init__(self, text):
        super().__init__("103c", text)


class BotApplicationIdInvalid(DisError):
    """BotApplicationIdInvalid
    Invalid bot application id
    """

    def __init__(self, text):
        super().__init__("104c", text)


class ApplicationIdIsNone(DisError):
    """ApplicationIdIsNone
    You don't type application id but you want to create application command
    """

    def __init__(self, text):
        super().__init__("105c", text)


class MessageComponentIsBlocked(DisError):
    """MessageComponentIsBlocked
    Message component is blocked to you
    """

    def __init__(self, text):
        super().__init__("106c", text)


# Package errors
class InvalidArgument(DisError):
    """InvalidArgument
    Invalid argument in method
    """

    def __init__(self, text):
        super().__init__("151p", text)


class ClassTypeError(DisError):
    """ClassTypeError
    Error with class type
    """

    def __init__(self, text):
        super().__init__("152p", text)


# User errors
class UserNitroTypeError(DisError):
    """UserNitroTypeError
    Invalid user nitro!
    """

    def __init__(self, text):
        super().__init__("201u", text)


# Json errors
class JsonError(DisError):
    """JsonError
    Error with json
    """

    def __init__(self, text):
        super().__init__("251j", text)


class ActivityUrlError(DisError):
    """ActivityUrlError
    Invalid activity url error
    """

    def __init__(self, text):
        super().__init__("252j", text)
