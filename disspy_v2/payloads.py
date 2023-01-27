from typing import TypedDict, NewType

from disspy_v2.enums import ApplicationCommandOptionType, ApplicationCommandType, ChannelType, MessageType

# Fixing bugs :)
_this = NewType('this', object)

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
    pass

class RolePayload(TypedDict):
    pass

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
    flags?	integer	message flags combined as a bitfield
    referenced_message?****	?message object	the message associated with the message_reference
    interaction?	message interaction object	sent if the message is a response to an Interaction
    thread?	channel object	the thread that was started from this message, includes thread member object
    components?**	array of message components	sent if the message contains components like buttons, action rows, or other interactive components
    sticker_items?	array of message sticker item objects	sent if the message contains stickers
    stickers?	array of sticker objects	Deprecated the stickers sent with the message
    position?	integer	A generally increasing integer (there may be gaps or duplicates) that represents the approximate position of the message in a thread, it can be used to estimate the relative position of the message in a thread in company with total_message_sent on parent thread
    role_subscription_data?	role subscription data object
