from typing import TYPE_CHECKING

from pytecord.role import Role

if TYPE_CHECKING:
    from pytecord.annotations import Snowflake
    from pytecord.payloads import GuildPayload

__all__ = (
    'Guild',
)

class WelcomeScreen: ...

class Guild:
    def __init__(self, data: 'GuildPayload') -> None:
        _ = data.get

        self.id: 'Snowflake' = _('id')
        self.name: str = _('name')
        self.icon: str | None = _('icon')
        self.icon_hash: str | None = _('icon_hash')
        self.splash: str | None = _('splash')
        self.discovery_splash: str | None = _('discovery_splash')
        self.owner: bool | None
        self.owner_id: Snowflake
        self.permissions: str | None
        self.afk_channel_id: Snowflake | None
        self.afk_timeout: int
        self.widget_enabled: bool | None
        self.widget_channel_id: Snowflake | None
        self.verification_level: int
        self.default_message_notifications: int
        self.explicit_content_filter: int
        self.roles: list[Role]
        # emojis: list[Emoji] TODO: Add emoji support
        self.features: list[str]
        self.mfa_level: int
        self.application_id: Snowflake | None
        self.system_channel_id: Snowflake | None
        self.system_channel_flags: int
        self.rules_channel_id: Snowflake | None
        self.max_presences: int | None
        self.max_members: int | None
        self.vanity_url_code: str | None
        self.description: str | None
        self.banner: str | None
        self.premium_tier: int
        self.premium_subscription_count: int | None
        self.preferred_locale: str
        self.public_updates_channel_id: Snowflake | None
        self.max_video_channel_users: int | None
        self.approximate_member_count: int | None
        self.approximate_presence_count: int | None
        self.welcome_screen: WelcomeScreen | None
        self.nsfw_level: int | None
        # stickers: list[Sticker] | None TODO: Add sticker support
        self.premium_progress_bar_enabled: bool
