__all__ = (
    'User',
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
    def __init__(self, session, **data) -> None:
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
