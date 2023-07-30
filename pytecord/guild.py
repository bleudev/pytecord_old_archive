from typing import Any

from pytecord.interfaces import Object

class Guild(Object):
    def __init__(self, data: dict[str, Any]):
        self.data = data

        self.id = int(data.get('id'))
        self.name = data.get('name')
        self.icon = data.get('icon')
        self.icon_hash = data.get('icon_hash')
        self.splash = data.get('splash')
        self.discovery_splash = data.get('discovery_splash')
        self.owner  = data.get('owner ')
        self.owner_id = data.get('owner_id')
        self.permissions  = data.get('permissions')
        self.region  = data.get('region ')
        self.afk_channel_id = int(data.get('afk_channel_id'))
        self.afk_timeout = data.get('afk_timeout')
        self.widget_enabled = data.get('widget_enabled')
        self.widget_channel_id = int(data.get('widget_channel_id'))
        self.verification_level = data.get('verification_level')
        self.default_message_notifications = data.get('default_message_notifications')
        self.explicit_content_filter = data.get('explicit_content_filter')
        self.roles = data.get('roles')
        self.emojis = data.get('emojis')
        self.features = data.get('features')
        self.mfa_level = data.get('mfa_level')
        self.application_id = int(data.get('application_id'))
        self.system_channel_id = int(data.get('system_channel_id'))
        self.system_channel_flags = data.get('system_channel_flags')
        self.rules_channel_id = int(data.get('rules_channel_id'))
        self.max_presences = data.get('max_presences')
        self.max_members = data.get('max_members')
        self.vanity_url_code = data.get('vanity_url_code')
        self.description = data.get('description')
        self.banner = data.get('banner')
        self.premium_tier = data.get('premium_tier')
        self.premium_subscription_count = data.get('premium_subscription_count')
        self.preferred_locale = data.get('preferred_locale')
        self.public_updates_channel_id = int(data.get('public_updates_channel_id'))
        self.max_video_channel_users = data.get('max_video_channel_users')
        self.max_stage_video_channel_users = data.get('max_stage_video_channel_users')
        self.approximate_member_count = data.get('approximate_member_count')
        self.approximate_presence_count = data.get('approximate_presence_count')
        self.welcome_screen = data.get('welcome_screen')
        self.nsfw_level = data.get('nsfw_level')
        self.stickers = data.get('stickers')
        self.premium_progress_bar_enabled = data.get('premium_progress_bar_enabled')
        self.safety_alerts_channel_id = int(data.get('safety_alerts_channel_id'))
    
    def __int__(self) -> int:
        """
        Returns a guild id

        ```
        >>> guild = Guild()
        >>> int(guild)
        ```
        """
        return self.id
    
    def eval(self) -> dict[str, Any]:
        """
        Returns a dict representation of object

        ```
        >>> guild = Guild()
        >>> guild.eval()
        ```
        """
        return self.data

class GuildChannel(Object):
    def __init__(self, data: dict[str, Any]):
        self.id = int(data.get('id'))
        self.type = data.get('type')
        self.guild_id = int(data.get('guild_id'))
        self.position = data.get('position')
        self.permission_overwrites = data.get('permission_overwrites')
        self.name = data.get('name')
        self.topic = data.get('topic')
        self.nsfw = data.get('nsfw')
        self.last_message_id = int(data.get('last_message_id'))
        self.bitrate = data.get('bitrate')
        self.user_limit = data.get('user_limit')
        self.rate_limit_per_user = data.get('rate_limit_per_user')
        self.recipients = data.get('recipients')
        self.icon = data.get('icon')
        self.owner_id = int(data.get('owner_id'))
        self.application_id = data.get('application_id')
        self.managed = data.get('managed')
        self.parent_id = int(data.get('parent_id'))
        self.last_pin_timestamp = data.get('last_pin_timestamp')
        self.rtc_region = data.get('rtc_region')
        self.video_quality_mode = data.get('video_quality_mode')
        self.message_count = data.get('message_count')
        self.member_count = data.get('member_count')
        self.thread_metadata = data.get('thread_metadata')
        self.member = data.get('member')
        self.default_auto_archive_duration = data.get('default_auto_archive_duration')
        self.permissions = data.get('permissions')
        self.flags = data.get('flags')
        self.total_message_sent = data.get('total_message_sent')
        self.available_tags = data.get('available_tags')
        self.applied_tags = data.get('applied_tags')
        self.default_reaction_emoji = data.get('default_reaction_emoji')
        self.default_thread_rate_limit_per_user = data.get('default_thread_rate_limit_per_user')
        self.default_sort_order = data.get('default_sort_order')
        self.default_forum_layout = data.get('default_forum_layout')

class Message:
    ...