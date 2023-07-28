from typing import TYPE_CHECKING, Any

from pytecord.role import Role
from pytecord.route import Route

if TYPE_CHECKING:
    from pytecord.payloads import GuildPayload, WelcomeScreenPayload, WelcomeScreenChannelPayload

__all__ = (
    'WelcomeChannel',
    'WelcomeScreen',
    'Guild',
)

class WelcomeChannel:
    def __init__(self, data: 'WelcomeScreenChannelPayload') -> None:
        _ = data.get

        self.channel_id: int = int( _('channel_id') )
        self.description: str = _('description')
        self.emoji_id: int | None = int( _('emoji_id') )
        self.emoji_name: str | None = _('emoji_name')

class WelcomeScreen:
    '''
    # Guild welcome screen object

    ### Magic operations

    ---

    `str()` -> Description of welcome screen
    
    `==` -> Welcome screens are equal
    
    `!=` -> Welcome screens aren't equal
    
    `in` -> Checks that WelcomeChannel in WelcomeScreen
    
    ```
    print(str(screen))

    print(screen1 == screen2)
    print(screen1 != screen2)

    if screen_channel in screen:
        print('Contains!')
    ```
    '''
    def __init__(self, session, data: 'WelcomeScreenPayload') -> None:
        _ = data.get

        self.description: str | None = _('description')
        self._channels: list[dict[str, Any]] = _('welcome_channels')

        self._session = session

    @property
    def channels(self) -> tuple[WelcomeChannel, ...]:
        '''
        Welcome screen channels

        Type: `tuple[WelcomeChannel, ...]`
        '''
        return (WelcomeChannel(i) for i in self._channels)

    def __str__(self) -> str:
        return self.description

    def __eq__(self, __value: 'WelcomeScreen') -> bool:
        return self.description == __value.description and self._channels == __value._channels

    def __ne__(self, __value: 'WelcomeScreen') -> bool:
        return self.description != __value.description or self._channels != __value._channels

    def __contains__(self, value: 'WelcomeChannel') -> bool:
        for i in self._channels:
            if int( i.get('channel_id') ) == value.channel_id:
                return True

        return False

class Guild:
    '''
    ## Guild object
    
    ### Magic operations

    ---
    
    `str()` -> Name of guild
    
    `int()` -> Guild id
    
    `repr()` -> Get repr string
    
    `==` -> Guilds are equal

    `!=` -> Guilds aren't equal
    
    ```
    print(str(guild))
    print(int(guild))
    
    print(repr(guild)) # or print(guild)
    
    print(guild1 == guild2)
    print(guild1 != guild2)
    ```
    '''
    def __init__(self, session, token: str, data: 'GuildPayload') -> None:
        _ = data.get

        self.id: int = int( _('id') )
        self.name: str = _('name')
        self.icon: str | None = _('icon')
        self.icon_hash: str | None = _('icon_hash')
        self.splash: str | None = _('splash')
        self.discovery_splash: str | None = _('discovery_splash')
        self.owner: bool | None = _('owner')
        self.owner_id: int = int( _('owner_id') )
        self.permissions: str | None = _('permissions')
        self.afk_channel_id: int | None = int( _('afk_channel_id') )
        self.afk_timeout: int = _('afk_timeout')
        self.widget_enabled: bool | None = _('widget_enabled')
        self.widget_channel_id: int | None = int( _('widget_channel_id') )
        self.verification_level: int = _('verification_level')
        self.default_message_notifications: int = _('default_message_notifications')
        self.explicit_content_filter: int = _('explicit_content_filter')
        self.features: list[str] = _('features')
        self.mfa_level: int = _('mfa_level')
        self.application_id: int | None = int( _('application_id') )
        self.system_channel_id: int | None = int( _('system_channel_id') )
        self.system_channel_flags: int = _('system_channel_flags')
        self.rules_channel_id: int | None = int( _('rules_channel_id') )
        self.max_presences: int | None = _('max_presences')
        self.max_members: int | None = _('max_members')
        self.vanity_url_code: str | None = _('vanity_url_code')
        self.description: str | None = _('description')
        self.banner: str | None = _('banner')
        self.premium_tier: int = _('premium_tier')
        self.premium_subscription_count: int | None = _('premium_subscription_count')
        self.preferred_locale: str = _('preferred_locale')
        self.public_updates_channel_id: int | None  = int( _('public_updates_channel_id') )
        self.max_video_channel_users: int | None = _('max_video_channel_users')
        self.approximate_member_count: int | None = _('approximate_member_count')
        self.approximate_presence_count: int | None = _('approximate_presence_count')
        self.welcome_screen: WelcomeScreen | None = WelcomeScreen(session, x) if (x := _('welcome_screen')) else None
        self.nsfw_level: int | None = _('nsfw_level')
        self.premium_progress_bar_enabled: bool = _('premium_progress_bar_enabled')

        self._roles: list[dict[str, Any]] = _('roles')
        self._emojis: list[dict[str, Any]] = _('emojis') # TODO: Add emoji support
        self._stickers: list[dict[str, Any]] | None = _('stickers') # TODO: Add sticker support

        self._session = session
        self._token = token

    def _sync(self) -> None:
        route = Route('/guilds/%d', self.id,
                      method='GET', token=self._token)
        _: 'GuildPayload' = route.request()[0].get

        self._roles = _('roles')
        self._emojis = _('emojis')
        self._stickers = _('stickers')

        self.id = int( _('id') )
        self.name = _('name')
        self.icon = _('icon')
        self.icon_hash = _('icon_hash')
        self.splash = _('splash')
        self.discovery_splash = _('discovery_splash')
        self.owner = _('owner')
        self.owner_id = int( _('owner_id') )
        self.permissions = _('permissions')
        self.afk_channel_id = int( _('afk_channel_id') )
        self.afk_timeout = _('afk_timeout')
        self.widget_enabled = _('widget_enabled')
        self.widget_channel_id = int( _('widget_channel_id') )
        self.verification_level = _('verification_level')
        self.default_message_notifications = _('default_message_notifications')
        self.explicit_content_filter = _('explicit_content_filter')
        self.features = _('features')
        self.mfa_level = _('mfa_level')
        self.application_id = int( _('application_id') )
        self.system_channel_id = int( _('system_channel_id') )
        self.system_channel_flags = _('system_channel_flags')
        self.rules_channel_id = int( _('rules_channel_id') )
        self.max_presences = _('max_presences')
        self.max_members = _('max_members')
        self.vanity_url_code = _('vanity_url_code')
        self.description = _('description')
        self.banner = _('banner')
        self.premium_tier = _('premium_tier')
        self.premium_subscription_count = _('premium_subscription_count')
        self.preferred_locale = _('preferred_locale')
        self.public_updates_channel_id  = int( _('public_updates_channel_id') )
        self.max_video_channel_users = _('max_video_channel_users')
        self.approximate_member_count = _('approximate_member_count')
        self.approximate_presence_count = _('approximate_presence_count')
        self.welcome_screen = WelcomeScreen(self._session, x) if (x := _('welcome_screen')) else None
        self.nsfw_level = _('nsfw_level')
        self.premium_progress_bar_enabled = _('premium_progress_bar_enabled')

    @property
    def roles(self) -> tuple[Role, ...]:
        '''
        Guild roles
        
        Type: `tuple[Role, ...]`
        '''
        self._sync()
        return (Role(self._session, **i) for i in self._roles)

    def __str__(self) -> str:
        self._sync()
        return self.name

    def __int__(self) -> int:
        return self.id

    def __repr__(self) -> str:
        self._sync()
        return f'Guild(name={self.name}, id={self.id}, owner={self.owner_id})'

    def __eq__(self, __value: 'Guild') -> bool:
        return self.id == __value.id

    def __ne__(self, __value: 'Guild') -> bool:
        return self.id != __value.id
