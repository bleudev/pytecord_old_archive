from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from disspy.payloads import RoleTagsPayload, RolePayload
    from aiohttp import ClientSession

__all__ = (
    'RoleTags',
    'Role',
)

class RoleTags:
    def __init__(self, **data: 'RoleTagsPayload') -> None:
        _ = data.get

        self.bot_id: int | None = _('bot_id')
        self.integration_id: int | None = _('integration_id')
        self.premium_subscriber: bool | None = _('premium_subscriber', False)
        self.subscription_listing_id: int | None = _('subscription_listing_id')
        self.available_for_purchase: bool | None = _('available_for_purchase', False)
        self.guild_connections: bool | None = _('guild_connections')

class Role:
    '''
    Guild role
    
    ### Magic operations
    ---
    
    `int()` -> Role id
    
    `str()` -> Role name
    
    ```
    int(role)
    str(role)
    ```
    '''
    def __init__(self, session: 'ClientSession', **data: 'RolePayload') -> None:
        self._session = session
        _ = data.get

        self.id: int = int(_('id')) # pylint: disable=invalid-name
        self.name: str = _('name')
        self.color: int = _('color', 0)
        self.hoist: bool = _('hoist', False)
        self.icon: str | None = _('icon')
        self.unicode_emoji: str | None = _('unicode_emoji')
        self.position: int = int(_('position'))
        self.permissions: str = _('permissions')
        self.managed: bool = _('managed', False)
        self.mentionable: bool = _('mentionable', False)
        self.tags: RoleTags | None = RoleTags(**x) if (x := _('tags')) else None # pylint: disable=invalid-name

    def __int__(self) -> int:
        return self.id
    def __str__(self) -> str:
        return self.name
