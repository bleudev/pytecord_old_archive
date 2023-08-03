from typing import Any

from .annotations import hash_str, permissions_set

class RoleTags:
    def __init__(self, data: dict[str, Any]) -> None:
        self.bot_id = int(x) if (x := data.get('bot_id')) else None
        self.integration_id = int(x) if (x := data.get('integration_id')) else None
        self.premium_subscriber = data.get('premium_subscriber')
        self.subscription_listing_id = int(x) if (x := data.get('subscription_listing_id')) else None
        self.available_for_purchase = data.get('available_for_purchase')
        self.guild_connections = data.get('guild_connections')


class Role:
    def __init__(self, data: dict[str, Any]):
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.color: int = data.get('color')
        self.hoist: bool = data.get('hoist')
        self.icon: hash_str | None = data.get('icon')
        self.unicode_emoji: str | None = data.get('unicode_emoji')
        self.position: int = data.get('position')
        self.permissions: permissions_set = data.get('permissions')
        self.managed: bool = data.get('managed')
        self.mentionable: bool = data.get('mentionable')
        self.tags: RoleTags = RoleTags(x) if (x := data.get('tags')) else None
        self.flags: int = data.get('flags')
