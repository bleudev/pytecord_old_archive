from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from disspy.payloads import UserPayload, GuildMemberPayload
    from aiohttp import ClientSession

__all__ = (
    'User',
    'Member',
)

class User:
    '''
    User object in discord API
    
    ### Magic operations
    ---
    
    `str()` -> User fullname

    `int()` -> User id
    
    ```
    str(user) # name#1234
    int(user) # 907966263270207519
    ```
    '''
    def __init__(self, session: 'ClientSession', **data: 'UserPayload') -> None:
        _ = data.get
        self._session = session

        self.id: int = int(_('id'))
        self.username: str = _('username')
        self.tag: str = _('discriminator')
        self.fullname: str = f'{self.username}#{self.tag}'
        self.bot: bool | None = _('bot', False)
        self.system: bool | None = _('system', False)
        self.mfa_enabled: bool | None = _('mfa_enabled', False)
        self.flags: int | None = _('flags', 0)
        self.public_flags: int | None = _('public_flags', 0)

    def __str__(self) -> str:
        return self.fullname
    def __int__(self) -> int:
        return self.id

class Member:
    '''
    Standart guild member in discord API
    
    ### Magic operations
    ---
    
    ...
    '''
    def __init__(self, session: 'ClientSession', user: User | None,**data: 'GuildMemberPayload') -> None:
        _ = data.get
        
        if not user:
            user = _('user')

        self.user: User | None = User(session, **user) if isinstance(user, dict) else user
        self.nick: str | None = nick if (nick := _('nick')) else self.user.username
        self.avatar: str | None = _('avatar')
        self.roles: list[str] = _('roles', [])
        self.joined_at: str = _('joined_at')
        self.premium_since: str | None = _('premium_since')
        self.deaf: bool = _('deaf', False)
        self.mute: bool = _('mute', False)
        self.pending: bool | None = _('pending', False)
        self.permissions: str | None = _('permissions', '0')
        self.communication_disabled_until: str | None = _('communication_disabled_until')

    def __str__(self) -> str:
        return self.nick
    def __int__(self) -> int:
        if self.user:
            return self.user.id
        return 0
