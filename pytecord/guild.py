from typing import Any, Literal

from .interfaces import Object
from .user import User, GuildMember
from .role import Role
from .reaction import Emoji, Sticker
from .utils import MessagePayload, get_snowflake, get_list_of_types, apost, rget
from .annotations import hash_str, permissions_set


class WelcomeScreenChannel:
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.description: str = data.get('description')
        self.emoji_id: int | None = get_snowflake('emoji_id')
        self.emoji_name: str | None = data.get('emoji_name')

        self.__channel_id = int(data.get('channel_id'))
        self.__token = token
    
    @property
    def channel(self) -> 'GuildChannel':
        data = rget(f'/channels/{self.__channel_id}', self.__token).json()
        return GuildChannel(data, self.__token)

class WelcomeScreen:
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.description: str | None = data.get('description')
        self.channels: list[WelcomeScreenChannel] = get_list_of_types(WelcomeScreenChannel, data.get('welcome_channels'), token)


class VerificationLevel:
    def __init__(self, integer: int) -> None:
        self.none: bool = integer == 0
        self.low: bool = integer == 1
        self.medium: bool = integer == 2
        self.high: bool = integer == 3
        self.very_high: bool = integer == 4

        self.__integer = integer
    
    def __int__(self) -> int:
        return self.__integer


class DefaultMessageNotificationLevel:
    def __init__(self, integer: int) -> None:
        self.all_messages = integer == 0
        self.only_mentions = integer == 1

        self.__integer = integer
    
    def __int__(self) -> int:
        return self.__integer


class ExplicitContentFilterLevel:
    def __init__(self, integer: int) -> None:
        self.disables = integer == 0
        self.members_without_roles = integer == 1
        self.all_members = integer == 2

        self.__integer = integer
    
    def __int__(self) -> int:
        return self.__integer


class NSFWLevel:
    def __init__(self, integer: int) -> None:
        self.default = integer == 0
        self.explicit = integer == 1
        self.safe = integer == 2
        self.age_restricted = integer == 3

        self.__integer = integer
    
    def __int__(self) -> int:
        return self.__integer


class GuildPreview(Object):
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.id: int = get_snowflake(data.get('id'))
        self.name: str = data.get('name')
        self.icon: str = data.get('icon')
        self.splash: str = data.get('splash')
        self.discovery_splash: str = data.get('discovery_splash')
        self.emojis: list[Emoji] = get_list_of_types(Emoji, data.get('emojis'), token)
        self.features: list[str] = data.get('features')
        self.approximate_member_count: int = data.get('approximate_member_count')
        self.approximate_presence_count: int = data.get('approximate_presence_count')
        self.description: str | None = data.get('description')
        self.stickers: list[Sticker] = get_list_of_types(Sticker, data.get('stickers'), token)


class Guild(Object):
    def __init__(self, data: dict[str, Any], token: str):
        self.id: int = get_snowflake(data.get('id'))
        self.name: str = data.get('name')
        self.icon: hash_str | None = data.get('icon')
        self.icon_hash: hash_str | None = data.get('icon_hash')
        self.splash: hash_str | None = data.get('splash')
        self.discovery_splash: hash_str | None = data.get('discovery_splash')
        self.is_owner: bool | None = data.get('owner')
        self.permissions: str | None = data.get('permissions')
        self.region: str | None = data.get('region') # deprecated
        self.afk_channel_id: int | None = get_snowflake(data.get('afk_channel_id'))
        self.afk_timeout: int = data.get('afk_timeout')
        self.widget_enabled: bool | None = data.get('widget_enabled')
        self.widget_channel_id: int | None = get_snowflake(x := data.get('widget_channel_id'))
        self.verification_level: VerificationLevel = VerificationLevel(data.get('verification_level'))
        self.default_message_notifications: DefaultMessageNotificationLevel = DefaultMessageNotificationLevel(data.get('default_message_notifications'))
        self.explicit_content_filter: ExplicitContentFilterLevel = ExplicitContentFilterLevel(data.get('explicit_content_filter'))
        self.features: list[str] = data.get('features')
        self.mfa_enabled: bool = data.get('mfa_level') == 1
        self.application_id: int | None = get_snowflake('application_id')
        self.system_channel_id: int | None = get_snowflake('system_channel_id')
        self.system_channel_flags: int = data.get('system_channel_flags')
        self.rules_channel_id: int | None = get_snowflake('rules_channel_id')
        self.max_presences: int | None = data.get('max_presences')
        self.max_members: int | None = data.get('max_members')
        self.vanity_url_code: str | None = data.get('vanity_url_code')
        self.description: str | None = data.get('description')
        self.banner: hash_str | None = data.get('banner')
        self.premium_tier:  int = data.get('premium_tier')
        self.premium_subscription_count: int | None = data.get('premium_subscription_count')
        self.preferred_locale: str = data.get('preferred_locale')
        self.public_updates_channel_id: int | None = int(data.get('public_updates_channel_id'))
        self.max_video_channel_users: int | None = data.get('max_video_channel_users')
        self.max_stage_video_channel_users: int | None = data.get('max_stage_video_channel_users')
        self.approximate_member_count: int | None = data.get('approximate_member_count')
        self.approximate_presence_count: int | None = data.get('approximate_presence_count')
        self.welcome_screen: WelcomeScreen | None = WelcomeScreen(x, token) if (x := data.get('welcome_screen')) else None
        self.nsfw_level: NSFWLevel = NSFWLevel(data.get('nsfw_level'))
        self.premium_progress_bar_enabled: bool = data.get('premium_progress_bar_enabled')
        self.safety_alerts_channel_id: int | None = get_snowflake('safety_alerts_channel_id')

        self.__owner_id = data.get('owner_id')
        self.__token = token
        self.__data = data
    
    @property
    def owner(self) -> User:
        data = rget(f'/users/{self.__owner_id}', self.__token).json()
        return User(data, self.__token)

    @property
    def channels(self) -> 'list[GuildChannel]':
        data = rget(f'/guilds/{self.id}/channels', self.__token).json()
        return get_list_of_types(GuildChannel, data, self.__token)

    @property
    def emojis(self) -> list[Emoji]:
        data = rget(f'/guilds/{self.id}/emojis', self.__token).json()
        return get_list_of_types(Emoji, data, self.__token)

    @property
    def roles(self) -> list[Role]:
        data = rget(f'/guilds/{self.id}/roles', self.__token).json()
        return get_list_of_types(Role, data)

    @property
    def stickers(self) -> list[Sticker]:
        data = rget(f'/guilds/{self.id}/stickers', self.__token).json()
        return get_list_of_types(Sticker, data, self.__token)
    
    @property
    def preview(self) -> GuildPreview:
        data = rget(f'/guilds/{self.id}/preview', self.__token).json()
        return GuildPreview(data, self.__token)

    def __int__(self) -> int:
        return self.id
    
    def __str__(self) -> str:
        return self.name
    
    def eval(self) -> dict[str, Any]:
        return self.__data
    
    def search(self, query: str, limit: int = 1) -> list[GuildMember] | GuildMember | None:
        """
        Returns a list of guild member objects whose username or nickname starts with a provided string

        https://discord.com/developers/docs/resources/guild#search-guild-members
        """
        payload = {
            'query': query,
            'limit': limit
        }
        data = rget(f'/guilds/{self.id}/members/search', self.__token, payload)

        result = get_list_of_types(GuildMember, data, self.__token, __default=[])
        if limit == 1 and len(result) == 1:
            result = result[0]
        elif len(result) == 0:
            result = None
        return result

class Overwrite:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = get_snowflake('id')
        self.type: Literal[0, 1] = data.get('type')
        self.str_type: Literal['role', 'member'] = 'role' if self.type == 0 else 'member'
        self.allow: permissions_set = data.get('allow')
        self.deny: permissions_set = data.get('deny')
    
    def __int__(self) -> int:
        return self.id


class GuildChannel(Object):
    def __init__(self, data: dict[str, Any], token: str):
        self.id: int = get_snowflake('id')
        self.type: int = data.get('type')
        self.position: int | None = data.get('position')
        self.permission_overwrites: list[Overwrite] = get_list_of_types(Overwrite, data.get('permission_overwrites', []))
        self.name = data.get('name')
        self.topic = data.get('topic')
        self.nsfw = data.get('nsfw')
        self.last_message_id = get_snowflake('last_message_id')
        self.bitrate = data.get('bitrate')
        self.user_limit = data.get('user_limit')
        self.rate_limit_per_user = data.get('rate_limit_per_user')
        self.recipients = get_list_of_types(User, data.get('recipients'), token)
        self.icon = data.get('icon')
        self.owner_id = get_snowflake('owner_id')
        self.application_id = get_snowflake('application_id')
        self.managed = data.get('managed')
        self.parent_id = get_snowflake('parent_id')
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

        self.__guild_id = get_snowflake('guild_id')
        self.__token = token
        self.__data = data
    
    @property
    def guild(self) -> Guild | None:
        if self.__guild_id:
            data = rget(f'/guilds/{self.__guild_id}', self.__token).json()
            return Guild(data, self.__token)
        return None
    
    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name

    def __getitem__(self, key: int)
        return self.fetch(key)
    
    def eval(self) -> dict[str, Any]:
        return self.__data
    
    def fetch(self, id: int) -> 'Message':
        """
        Fetch a message

        ```
        >>> channel = GuildChannel()
        >>> message = channel.fetch(955886808095399996)
        ```
        """
        data = rget(f'/channels/{self.id}/messages/{id}', self.__token).json()
        return Message(data, self.__token)
    
    async def send(self, content: str) -> 'Message':
        payload = MessagePayload(content)
        data = await apost(f'/channels/{self.id}/messages', self.__token, data=payload.eval())
        return Message(data, self.__token)

class Message:
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.id = get_snowflake('id')
        self.author = User(data.get('author'), token)
        self.content = data.get('content')
        self.timestamp = data.get('timestamp')
        self.edited_timestamp = data.get('edited_timestamp')
        self.tts = data.get('tts')
        self.mention_everyone = data.get('mention_everyone')
        self.mentions = get_list_of_types(User, data.get('mentions'), token)
        self.mention_roles = data.get('mention_roles')
        self.mention_channels = data.get('mention_channels')
        self.attachments = data.get('attachments')
        self.embeds = data.get('embeds')
        self.reactions = data.get('reactions')
        self.nonce = data.get('nonce')
        self.pinned = data.get('pinned')
        self.webhook_id = get_snowflake('webhook_id')
        self.type = data.get('type')
        self.activity = data.get('activity')
        self.application = data.get('application')
        self.application_id = get_snowflake('application_id')
        self.message_reference = data.get('message_reference')
        self.flags = data.get('flags')
        self.referenced_message = data.get('referenced_message')
        self.interaction = data.get('interaction')
        self.thread = data.get('thread')
        self.components = data.get('components')
        self.sticker_items = data.get('sticker_items')
        self.stickers = data.get('stickers')
        self.position = data.get('position')
        self.role_subscription_data = data.get('role_subscription_data')

        # Extra fields for message create
        self.guild_id = get_snowflake('guild_id')
        self.member = data.get('member')

        self.__channel_id = data.get('channel_id')
        self.__token = token
        self.__data = data

    @property
    def channel(self) -> GuildChannel:
        data = rget(f'/channels/{self.__channel_id}', self.__token).json()
        return GuildChannel(data, self.__token)
    
    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.content
    
    def eval(self) -> dict[str, Any]:
        return self.__data
    
    async def reply(self, content: str) -> 'Message':
        payload = MessagePayload(content)
        payload.make_reply(self.id)
        data = await apost(f'/channels/{self.__channel_id}/messages', self.__token, data=payload.eval())
        return Message(data, self.__token)

class MessageDeleteEvent:
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.id = get_snowflake('id')

        self.__channel_id = int(data.get('channel_id'))
        self.__guild_id = get_snowflake('guild_id')
        self.__token = token
    
    @property
    def channel(self) -> GuildChannel:
        data = rget(f'/channels/{self.__channel_id}', self.__token).json()
        return GuildChannel(data, self.__token)
    
    @property
    def guild(self) -> Guild:
        data = rget(f'/guilds/{self.__guild_id}', self.__token).json()
        return Guild(data, self.__token)

    def __int__(self) -> int:
        return self.id
