'''
Json dict payloads like objects in discord API
'''

from typing import Literal, NewType, TypedDict

from disspy.enums import (ApplicationCommandOptionType, ApplicationCommandType,
                          ApplicationFlags, ButtonStyle, ChannelFlags,
                          ChannelType, ComponentType, EmbedType,
                          GuildForumLayoutType, GuildForumSortOrderType,
                          InteractionType, MessageActivityType, MessageFlags,
                          MessageType, NitroPremiumType, OverwriteType,
                          StickerFormatType, StickerType,
                          TeamMemberMembershipState, TextInputStyle, UserFlags,
                          VideoQualityMode)

# Fixing bugs :)
_this = NewType('_this', type)
_MessageComponentPayload = NewType('_MessageComponentPayload', type)
_StickerPayload = NewType('_StickerPayload', type)

# Typing
HashStr = NewType('HashStr', str)
IntColor = NewType('IntColor', int)
LocaleStr = NewType('LocaleStr', str)
BitSet = NewType('BitSet', str)
UnicodeStr = NewType('UnicodeStr', str)
Iso8601Timestamp = NewType('Iso8601Timestamp', str)

class ApplicationCommandOptionChoicePayload(TypedDict):
    '''
    Application command option choice payload
    '''
    name: str
    name_localizations: dict[str, str] | None
    value: str | int | float

class ApplicationCommandOptionPayload(TypedDict):
    '''
    Application command option payload
    '''
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
    '''
    Application command payload
    '''
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
    '''
    User payload
    '''
    id: int
    username: str
    discriminator: str
    avatar: HashStr | None
    bot: bool | None
    system: bool | None
    mfa_enabled: bool | None
    banner: HashStr | None
    accent_color: IntColor | None
    locale: LocaleStr
    # Needs email Oauth2 scope
    verified: bool | None
    email: str | None
    #
    flags: UserFlags | None
    premium_type: NitroPremiumType | None
    public_flags: UserFlags | None

class RoleTagsPayload(TypedDict):
    '''
    Role tags payload
    '''
    bot_id: int | None
    integration_id: int | None
    premium_subscriber: bool | None
    subscription_listing_id: int | None
    available_for_purchase: bool | None
    guild_connections: bool | None

class RolePayload(TypedDict):
    '''
    Role payload
    '''
    id: int
    name: str
    color: IntColor
    hoist: bool
    icon: HashStr | None
    unicode_emoji: UnicodeStr | None
    position: int
    permissions: BitSet
    managed: bool
    mentionable: bool
    tags: RoleTagsPayload | None

class ChannelMentionPayload(TypedDict):
    '''
    Channel mention payload
    '''
    id: int
    guild_id: int
    type: ChannelType
    name: str

class AttachmentPayload(TypedDict):
    '''
    Attachment payload
    '''
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
    '''
    Message embed footer payload
    '''
    text: str
    icon_url: str | None
    proxy_icon_url: str | None

class EmbedImagePayload(TypedDict):
    '''
    Message embed image payload
    '''
    url: str
    proxy_url: str | None
    height: int | None
    width: int | None

class EmbedThumbnailPayload(TypedDict):
    '''
    Message embed thumbnail payload
    '''
    url: str
    proxy_url: str | None
    height: int | None
    width: int | None

class EmbedVideoPayload(TypedDict):
    '''
    Message embed video payload
    '''
    url: str | None
    proxy_url: str | None
    height: int | None
    width: int | None

class EmbedProviderPayload(TypedDict):
    '''
    Message embed provider payload
    '''
    name: str | None
    url: str | None

class EmbedAuthorPayload(TypedDict):
    '''
    Message embed author payload
    '''
    name: str
    url: str | None
    icon_url: str | None
    proxy_icon_url: str | None

class EmbedFieldPayload(TypedDict):
    '''
    Message embed field payload
    '''
    name: str
    value: str
    inline: bool | None

class EmbedPayload(TypedDict):
    '''
    Message embed payload
    '''
    title: str | None
    type: EmbedType | None
    description: str | None
    url: str | None
    timestamp: Iso8601Timestamp | None
    color: IntColor | None
    footer: EmbedFooterPayload | None
    image: EmbedImagePayload | None
    thumbnail: EmbedThumbnailPayload | None
    video: EmbedVideoPayload | None
    provider: EmbedProviderPayload | None
    author: EmbedAuthorPayload | None
    fields: list[EmbedFieldPayload] | None

class EmojiPayload(TypedDict):
    '''
    Emoji payload
    '''
    id: int
    name: str | None
    roles: list[int] | None
    user: UserPayload | None
    require_colons: bool | None
    managed: bool | None
    animated: bool | None
    available: bool | None

class ReactionPayload(TypedDict):
    '''
    Message reaction payload
    '''
    count: int
    me: bool
    emoji: EmojiPayload

class MessageActivityPayload(TypedDict):
    '''
    Message activity payload
    '''
    type: MessageActivityType
    party_id: str | None

class TeamMemberPayload(TypedDict):
    '''
    Application team member payload
    '''
    membership_state: TeamMemberMembershipState
    permissions: list[str]
    team_id: int
    user: UserPayload

class TeamPayload(TypedDict):
    '''
    Application team payload
    '''
    icon: HashStr | None
    id: int
    members: list[TeamMemberPayload]
    name: str
    owner_user_id: int

class InstallParamsPayload(TypedDict):
    '''
    Application install params payload
    '''
    scopes: list[str]
    permissions: str

class ApplicationPayload(TypedDict):
    '''
    Application payload
    '''
    id: int
    name: str
    icon: HashStr | None
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
    cover_image: HashStr | None
    flags: ApplicationFlags | None
    tags: list[str] | None
    install_params: InstallParamsPayload | None
    custom_install_url: str | None
    role_connections_verification_url: str | None

class MessageReferencePayload(TypedDict):
    '''
    Message reference payload
    '''
    message_id: int | None
    channel_id: int | None
    guild_id: int | None
    fail_if_not_exists: bool | None

class GuildMemberPayload(TypedDict):
    '''
    Guild member payload
    '''
    user: UserPayload | None
    nick: str | None
    avatar: HashStr | None
    roles: list[int]
    joined_at: Iso8601Timestamp
    premium_since: Iso8601Timestamp | None
    deaf: bool
    mute: bool
    pending: bool | None
    permissions: str | None
    communication_disabled_until: Iso8601Timestamp | None

class MessageInteractionPayload(TypedDict):
    '''
    Message interaction payload
    '''
    id: int
    type: InteractionType
    name: str
    user: UserPayload
    member: GuildMemberPayload | None

class OverwritePayload(TypedDict):
    '''
    Channel overwrite payload
    '''
    id: int
    type: OverwriteType
    allow: str
    deny: str

class ThreadMetadataPayload(TypedDict):
    '''
    Thread (channel with 10-12 type) metadata payload
    '''
    archived: bool
    auto_archive_duration: Literal[60, 1440, 4320, 10080]
    archive_timestamp: Iso8601Timestamp
    locked: bool
    invitable: bool | None
    create_timestamp: Iso8601Timestamp | None

class ThreadMemberPayload(TypedDict):
    '''
    Thread (channel with 10-12 type) member payload
    '''
    id: int | None
    user_id: int | None
    join_timestamp: Iso8601Timestamp
    flags: int
    member: GuildMemberPayload | None

class ForumTagPayload(TypedDict):
    '''
    Forum (channel with 15 type) tag payload
    '''
    id: int
    name: str
    moderated: bool
    emoji_id: int | None
    emoji_name: str | None

class ChannelPayload(TypedDict):
    '''
    Channel payload
    '''
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
    icon: HashStr | None
    owner_id: int | None
    application_id: int | None
    parent_id: int | None
    last_pin_timestamp: Iso8601Timestamp | None
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
    applied_tags: list[int] | None
    default_reaction_emoji: ReactionPayload | None
    default_thread_rate_limit_per_user: int | None
    default_sort_order: GuildForumSortOrderType | None
    default_forum_layout: GuildForumLayoutType | None

# Message components
class ActionRowPayload(TypedDict):
    '''
    Action row component payload
    '''
    type: Literal[1]
    components: list[_MessageComponentPayload]

class ButtonPayload(TypedDict):
    '''
    Button component payload
    '''
    type: Literal[2]
    style: ButtonStyle
    label: str | None
    emoji: EmojiPayload | None
    custom_id: str | None
    url: str | None
    disabled: bool | None

class SelectOptionPayload(TypedDict):
    '''
    Select menu option payload
    '''
    label: str
    value: str
    description: str | None
    emoji: EmojiPayload | None
    default: bool | None

class SelectMenuPayload(TypedDict):
    '''
    Select menu component payload
    '''
    type: Literal[3, 5, 6, 7, 8]
    custom_id: str
    options: list[SelectOptionPayload] | None
    channel_types: list[ChannelType] | None
    placeholder: str | None
    min_values: int | None
    max_values: int | None
    disabled: bool | None

class TextInputPayload(TypedDict):
    '''
    Text input component payload
    '''
    type: Literal[4]
    custom_id: str
    style: TextInputStyle
    label: str
    min_length: int | None
    max_length: int | None
    required: bool | None
    value: str | None
    placeholder: str | None
# # # # # #

class MessageComponentPayload(TypedDict):
    '''
    Message component payload
    '''
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
    '''
    Message sticker item payload
    '''
    id: int
    name: str
    format_type: StickerFormatType

class StickerPackPayload(TypedDict):
    '''
    Message sticker pack payload
    '''
    id: int
    stickers: list[_StickerPayload]
    name: str
    sku_id: int
    cover_sticker_id: int | None
    description: str
    banner_asset_id: int | None

class StickerPayload(TypedDict):
    '''
    Message sticker payload
    '''
    id: int
    pack_id: int | None
    name: str
    description: str | None
    tags: str
    asset: str # Deprecated
    type: StickerType
    format_type: StickerFormatType
    available: bool | None
    guild_id: int | None
    user: UserPayload | None
    sort_value: int | None

class RoleSubscriptionData(TypedDict):
    '''
    Role subscription data in message
    '''
    role_subscription_listing_id: int
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool

class MessagePayload(TypedDict):
    '''
    Channel message payload
    '''
    id: int
    channel_id: int
    author: UserPayload
    content: str | None
    timestamp: Iso8601Timestamp
    edited_timestamp: Iso8601Timestamp | None
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
