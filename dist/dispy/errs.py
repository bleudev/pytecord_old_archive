from typing import Optional

# Constants for messages
missingperms = "Missing permissions!"


# Parent for all errors
class _DisRunTimeError(RuntimeWarning):
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
class InternetError(_DisRunTimeError):
    def __init__(self, text, code: Optional[str] = None):
        if code is None:
            super().__init__("-1i", text)
        else:
            super().__init__(code, text)


class MissingPerms(_DisRunTimeError):
    def __init__(self, text):
        super().__init__("-2i", text)


# Client errors
class BotPrefixError(_DisError):
    def __init__(self, text):
        super().__init__("101c", text)


class BotTypeError(_DisError):
    def __init__(self, text):
        super().__init__("102c", text)


class BotEventTypeError(_DisError):
    def __init__(self, text):
        super().__init__("103c", text)


class BotStatusError(_DisError):
    def __init__(self, text):
        super().__init__("104c", text)


# User errors
class UserNitroTypeError(_DisError):
    def __init__(self, text):
        super().__init__("201u", text)
