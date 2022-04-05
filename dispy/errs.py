class TokenError(Exception):
    def __init__(self, text):
        self.__code__ = "100c"
        self.__text__ = text
        self.__message__ = f"{self.__code__} - {self.__text__}"

        super().__init__(self.__message__)


class SendError(Exception):
    def __init__(self, text):
        self.__code__ = "102c"
        self.__text__ = text
        self.__message__ = f"{self.__code__} - {self.__text__}"

        super().__init__(self.__message__)


class PrefixError(Exception):
    def __init__(self, text):
        self.__code__ = "101c"
        self.__text__ = text
        self.__message__ = f"{self.__code__} - {self.__text__}"

        super().__init__(self.__message__)
