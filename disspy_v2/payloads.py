from typing import TypedDict, NewType

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
)

# Fixing bugs :)
_this = NewType('this', object)

# Typing
hashStr = NewType('hashStr', str)
intColor = NewType('intColor', int)
localeStr = NewType('localeStr', str)
bitSet = NewType('bitSet', str)
unicodeStr = NewType('unicodeStr', str)

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
    timestamp: str | None
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
    tags?	array of strings	up to 5 tags describing the content and functionality of the application
    install_params?	install params object	settings for the application's default in-app authorization link, if enabled
    custom_install_url?	string	the application's default custom authorization link, if enabled
    role_connections_verification_url?	string

class MessageReferencePayload(TypedDict):
    pass

class MessageInteractionPayload(TypedDict):
    pass

class ChannelPayload(TypedDict):
    pass

class MessageComponentPayload(TypedDict):
    pass

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
    timestamp: str
    edited_timestamp: str | None
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
