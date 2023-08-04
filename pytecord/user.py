from typing import Any

from .interfaces import Object
from .annotations import hash_str
from .utils import get_snowflake

class User(Object):
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.id: int = get_snowflake('id')
        self.username: str = data.get('username')
        self.discriminator: str | None = data.get('discriminator')
        self.global_name: str | None = data.get('global_name')
        self.avatar: hash_str | None = data.get('avatar')
        self.bot: bool | None = data.get('bot')
        self.system: bool | None = data.get('system')
        self.mfa_enabled: bool | None = data.get('mfa_enabled')
        self.banner: hash_str | None = data.get('banner')
        self.accent_color: int | None = data.get('accent_color')
        self.locale: str | None = data.get('locale')
        self.verified: bool | None = data.get('verified')
        self.email: str | None = data.get('email')
        self.flags: int | None = data.get('flags')
        self.premium_type: int | None = data.get('premium_type')
        self.public_flags: int | None = data.get('public_flags')
        self.avatar_decoration: hash_str | None = data.get('avatar_decoration')

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
        return self.id
