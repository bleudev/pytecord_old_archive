class User:
    '''
User
----

::

    async def on_ready(user: User):
        print(str(user)) # Bot user fullname

User object in discord API

`username` - Display username in profile

`tag` - Discord 4-digit tag
    '''
    def __init__(self, session, **data) -> None:
        _ = data.get
        self._session = session

        self.id: int = _('id')
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
