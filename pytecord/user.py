from typing import Any

from .interfaces import Object


class User(Object):
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.__token = token
        self.__data = data
    
    def eval(self) -> dict[str, Any]:
        """
        Returns a dict representation of user

        ```
        >>> user = User()
        >>> user.eval()
        ```
        """
        return self.__data
    
    def __int__(self) -> int:
        """
        Returns an object id

        ```
        >>> obj = Object()
        >>> int(obj)
        ```
        """
        print('Is under developerment!')
        return 0
