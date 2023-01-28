from typing import TypedDict, NewType, Literal

from disspy_v2.enums import (
    ApplicationCommandOptionType,
    ApplicationCommandType,
    ChannelType,
    MessageType,
    MessageFlags,
    UserFlags,
    NitroPremiumType,
    EmbedType,
    MessageActivityType,
    TeamMemberMembershipState,
    ApplicationFlags,
    InteractionType,
    OverwriteType,
    ChannelFlags,
    GuildForumSortOrderType,
    GuildForumLayoutType,
    VideoQualityMode,
    ComponentType,
    ButtonStyle,
    TextInputStyle
)

# Fixing bugs :)
_this = NewType('this', type)
_MessageComponentPayload = NewType('MessageComponentPayload', type)

# Typing
hashStr = NewType('hashStr', str)
intColor = NewType('intColor', int)
localeStr = NewType('localeStr', str)
bitSet = NewType('bitSet', str)
unicodeStr = NewType('unicodeStr', str)
iso8601_timestamp = NewType('iso8601_timestamp', str)

class ApplicationCommandOptionChoicePayload(TypedDict):
    name: str
    name_localizations: dict[str, str] | None
    value: str | int | float

class ApplicationCommandOptionPayload(TypedDict):
    type: ApplicationCommandOptionType
    name: str
    name_localizations: dict[str, str] | None
    description: str
    description_localizations: dict[str, str] | None
    required: bool | None
    choices: list[ApplicationCommandOptionChoicePayload] | None
    options: list[_this] | None
    channel_types: list[ChannelType] | None
    min_value: int | float | None
    max_value: int | float | None
    min_length: int | None
    max_length: int | None
    autocomplete: bool | None

class ApplicationCommandPayload(TypedDict):
    id: int
    type: ApplicationCommandType | None
    application_id: int
    guild_id: int | None
    name: str
    name_localizations: dict[str, str] | None
    description: str | None
    description_localizations: dict[str, str] | None
    options: list[ApplicationCommandOptionPayload] | None
    default_member_permissions: str | None
    dm_permission: bool | None
    default_permission: bool | None
    nsfw: bool | None
    version: int

class UserPayload(TypedDict):
    id: int
    username: str
    discriminator: str
    avatar: hashStr | None
    bot: bool | None
    system: bool | None
    mfa_enabled: bool | None
    banner: hashStr | None
    accent_color: intColor | None
    locale: localeStr
    # Needs email Oauth2 scope
    verified: bool | None
    email: str | None
    #
    flags: UserFlags | None
    premium_type: NitroPremiumType | None
    public_flags: UserFlags | None

class RoleTagsPayload(TypedDict):
    bot_id: int | None
    integration_id: int | None
    premium_subscriber: bool | None
    subscription_listing_id: int | None
    available_for_purchase: bool | None
    guild_connections: bool | None

class RolePayload(TypedDict):
    id: int
    name: str
    color: intColor
    hoist: bool
    icon: hashStr | None
    unicode_emoji: unicodeStr | None
    position: int
    permissions: bitSet
    managed: bool
    mentionable: bool
    tags: RoleTagsPayload | None

class ChannelMentionPayload(TypedDict):
    id: int
    guild_id: int
    type: ChannelType
    name: str

class AttachmentPayload(TypedDict):
    id: int
    filename: str
    description: str | None
    content_type: str | None
    size: int
    url: str
    proxy_url: str
    height: int | None
    width: int | None
    ephemeral: bool | None

class EmbedFooterPayload(TypedDict):
    text: str
    icon_url: str | None
    proxy_icon_url: str | None

class EmbedImagePayload(TypedDict):
    url: str
    proxy_url: str | None
    height: int | None
    width: int | None

class EmbedThumbnailPayload(TypedDict):
    url: str
    proxy_url: str | None
    height: int | None
    width: int | None

class EmbedVideoPayload(TypedDict):
    url: str | None
    proxy_url: str | None
    height: int | None
    width: int | None

class EmbedProviderPayload(TypedDict):
    name: str | None
    url: str | None

class EmbedAuthorPayload(TypedDict):
    name: str
    url: str | None
    icon_url: str | None
    proxy_icon_url: str | None

class EmbedFieldPayload(TypedDict):
    name: str
    value: str
    inline: bool | None

class EmbedPayload(TypedDict):
    title: str | None
    type: EmbedType | None
    description: str | None
    url: str | None
    timestamp: iso8601_timestamp | None
    color: intColor | None
    footer: EmbedFooterPayload | None
    image: EmbedImagePayload | None
    thumbnail: EmbedThumbnailPayload | None
    video: EmbedVideoPayload | None
    provider: EmbedProviderPayload | None
    author: EmbedAuthorPayload | None
    fields: list[EmbedFieldPayload] | None

class EmojiPayload(TypedDict):
    id: int
    name: str | None
    roles: list[RolePayload.id] | None
    user: UserPayload | None
    require_colons: bool | None
    managed: bool | None
    animated: bool | None
    available: bool | None

class ReactionPayload(TypedDict):
    count: int
    me: bool
    emoji: EmojiPayload

class MessageActivityPayload(TypedDict):
    type: MessageActivityType
    party_id: str | None

class TeamMemberPayload(TypedDict):
    membership_state: TeamMemberMembershipState
    permissions: list[str]
    team_id: int
    user: UserPayload

class TeamPayload(TypedDict):
    icon: hashStr | None
    id: int
    members: list[TeamMemberPayload]
    name: str
    owner_user_id: int

class InstallParamsPayload(TypedDict):
    scopes: list[str]
    permissions: str

class ApplicationPayload(TypedDict):
    id: int
    name: str
    icon: hashStr | None
    description: str
    rpc_origins: list[str] | None
    bot_public: bool
    bot_require_code_grant: bool
    terms_of_service_url: str | None
    privacy_policy_url: str | None
    owner: UserPayload
    summary: str # Soon will be removed in v11!
    verify_key: str
    team: TeamPayload | None
    guild_id: int | None
    primary_sku_id: int | None
    slug: str | None
    cover_image: hashStr | None
    flags: ApplicationFlags | None
    tags: list[str] | None
    install_params: InstallParamsPayload | None
    custom_install_url: str | None
    role_connections_verification_url: str | None

class MessageReferencePayload(TypedDict):
    message_id: int | None
    channel_id: int | None
    guild_id: int | None
    fail_if_not_exists: bool | None

class GuildMemberPayload(TypedDict):
    user: UserPayload | None
    nick: str | None
    avatar: hashStr | None
    roles: list[RolePayload.id]
    joined_at: iso8601_timestamp
    premium_since: iso8601_timestamp | None
    deaf: bool
    mute: bool
    pending: bool | None
    permissions: str | None
    communication_disabled_until: iso8601_timestamp | None

class MessageInteractionPayload(TypedDict):
    id: int
    type: InteractionType
    name: str
    user: UserPayload      
    member: GuildMemberPayload | None

class OverwritePayload(TypedDict):
    id: int
    type: OverwriteType
    allow: str
    deny: str

class ThreadMetadataPayload(TypedDict):
    archived: bool
    auto_archive_duration: Literal[60, 1440, 4320, 10080]
    archive_timestamp: iso8601_timestamp
    locked: bool
    invitable: bool | None
    create_timestamp: iso8601_timestamp | None

class ThreadMemberPayload(TypedDict):
    id: int | None
    user_id: int | None
    join_timestamp: iso8601_timestamp
    flags: int
    member: GuildMemberPayload | None

class ForumTagPayload(TypedDict):
    id: int
    name: str
    moderated: bool
    emoji_id: int | None
    emoji_name: str | None

class ChannelPayload(TypedDict):
    id: int
    type: ChannelType
    guild_id: int | None
    position: int | None
    permission_overwrites: list[OverwritePayload] | None
    name: str | None
    topic: str | None
    nsfw: bool | None
    last_message_id: int | None
    bitrate: int | None
    user_limit: int | None
    rate_limit_per_user: int | None
    recipients: list[UserPayload] | None
    icon: hashStr | None
    owner_id: int | None
    application_id: int | None
    parent_id: int | None
    last_pin_timestamp: iso8601_timestamp | None
    rtc_region: str | None
    video_quality_mode: VideoQualityMode | None
    message_count: int | None
    member_count: int | None
    thread_metadata: ThreadMetadataPayload | None
    member: ThreadMemberPayload | None
    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None
    permissions: str | None
    flags: ChannelFlags | None
    total_message_sent: int | None
    available_tags: list[ForumTagPayload] | None
    applied_tags: list[ForumTagPayload.id] | None
    default_reaction_emoji: ReactionPayload | None
    default_thread_rate_limit_per_user: int | None
    default_sort_order: GuildForumSortOrderType | None
    default_forum_layout: GuildForumLayoutType | None

# Message components
class ActionRowPayload(TypedDict):
    type: Literal[1]
    components: list[_MessageComponentPayload]

class ButtonPayload(TypedDict):
    type: Literal[2]
    style: ButtonStyle
    label: str | None
    emoji: EmojiPayload | None
    custom_id: str | None
    url: str | None
    disabled: bool | None

class SelectOptionPayload(TypedDict):
    label: str
    value: str
    description: str | None
    emoji: EmojiPayload | None
    default: bool | None

class SelectMenuPayload(TypedDict):
    type: Literal[3, 5, 6, 7, 8]
    custom_id: str
    options: list[SelectOptionPayload] | None
    channel_types: list[ChannelType] | None
    placeholder: str | None
    min_values: int | None
    max_values: int | None
    disabled: bool | None

class TextInputPayload(TypedDict):
    type: Literal[4]
    custom_id: str
    style: TextInputStyle
    label: str
    min_length: int | None
    max_length: int | None
    required: bool | None
    value: str | None
    placeholder: str | None
#

class MessageComponentPayload(TypedDict):
    type: ComponentType
    components: list[_this]
    style: ButtonStyle | TextInputStyle | None
    label: str | None
    emoji: EmojiPayload | None
    custom_id: str | None
    url: str | None
    disabled: bool | None
    options: list[SelectOptionPayload] | None
    channel_types: list[ChannelType] | None
    placeholder: str | None
    min_values: int | None
    max_values: int | None
    min_length: int | None
    max_length: int | None
    required: bool | None
    value: str | None

class MessageStickerItemPayload(TypedDict):
    pass

class StickerPayload(TypedDict):
    pass

class RoleSubscriptionData(TypedDict):
    pass

class MessagePayload(TypedDict):
    id: int
    channel_id: int
    author: UserPayload
    content: str | None
    timestamp: iso8601_timestamp
    edited_timestamp: iso8601_timestamp | None
    tts: bool
    mention_everyone: bool
    mentions: list[UserPayload] | None
    mention_roles: list[RolePayload] | None
    mention_channels: list[ChannelMentionPayload] | None
    attachments: list[AttachmentPayload] | None
    embeds: list[EmbedPayload] | None
    reactions: list[ReactionPayload] | None
    nonce: int | str | None
    pinned: bool
    webhook_id: int | None
    type: MessageType
    activity: MessageActivityPayload | None
    application: ApplicationPayload | None
    application_id: int | None
    message_reference: MessageReferencePayload | None
    flags: MessageFlags
    referenced_message: _this | None
    interaction: MessageInteractionPayload | None
    thread: ChannelPayload | None
    components: list[MessageComponentPayload] | None
    sticker_items: list[MessageStickerItemPayload] | None
    stickers: list[StickerPayload] | None
    position: int | None
    role_subscription_data: RoleSubscriptionData | None
