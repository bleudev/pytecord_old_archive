from typing import TypedDict, NewType

from disspy_v2.enums import (
    ApplicationCommandOptionType,
    ApplicationCommandType,
    ChannelType,
    MessageType,
    MessageFlags,
    UserFlags,
    NitroPremiumType,
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
    pass

class AttachmentPayload(TypedDict):
    pass

class EmbedPayload(TypedDict):
    pass

class ReactionPayload(TypedDict):
    pass

class MessageActivityPayload(TypedDict):
    pass

class ApplicationPayload(TypedDict):
    pass

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
