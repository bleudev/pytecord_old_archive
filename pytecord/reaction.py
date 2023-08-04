from typing import Any
from .role import Role
from .user import User
from .utils import get_snowflake, get_list_of_types

class Emoji:
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.id: int = get_snowflake('id')
        self.name: str | None = data.get('name')
        self.roles: list[Role] | None = get_list_of_types(Role, data.get('roles'))
        self.user: User = User(data.get('user'), token)
        self.require_colons: bool | None = data.get('require_colons')
        self.managed: bool | None = data.get('managed')
        self.animated: bool | None = data.get('animated')
        self.available: bool | None = data.get('available')


class Sticker:
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.id: int = get_snowflake('id')
        self.pack_id = get_snowflake('pack_id') 
        self.name: str = data.get('name')
        self.description: str | None = data.get('description')
        self.tags: str = data.get('tags')
        self.asset: str = data.get('asset')  # deprecated
        self.type: int = data.get('type')
        self.format_type: int = data.get('format_type')
        self.available: bool | None = data.get('available')
        self.guild_id: int | None = get_snowflake('guild_id')
        self.user: User | None = User(x, token) if (x := data.get('user')) else None
        self.sort_value: int | None = data.get('sort_value')
