class InteractionType:
    ping = 1
    application_command = 2
    message_component = 3
    application_command_autocomplete = 4
    modal_submit = 5

class InteractionCallbackType:
    pong = 1
    channel_message_with_source = 4
    deferred_channel_message_with_source = 5
    deferred_update_message = 6
    update_message = 7
    application_command_autocomplete_result = 8
    modal = 9

class ComponentType:
    action_row = 1
    button = 2
    string_select = 3
    text_input = 4
    user_select  = 5
    role_select = 6
    mentionable_select = 7
    channel_select = 8

class ApplicationCommandType:
    chat_input = 1
    user = 2
    message = 3

class ApplicationCommandOptionType:
    sub_command = 1
    sub_command_group = 2
    string = 3
    integer = 4
    boolean = 5
    user = 6
    channel = 7
    role = 8
    mentionable = 9
    number = 10
    attachment = 11

class ChannelType:
    guild_text = 0
    dm = 1
    guild_voice = 2
    group_dm = 3
    guild_category = 4
    guild_announcement = 5
    announcement_thread = 10
    public_thread = 11
    private_thread = 12
    guild_stage_voice = 13
    guild_directory = 14
    guild_forum = 15

class MessageType:
    default = 0
    recipient_add = 1
    recipient_remove = 2
    call = 3
    channel_name_change = 4
    channel_icon_change = 5
    channel_pinned_message = 6
    user_join = 7
    guild_boost = 8
    guild_boost_tier_1 = 9
    guild_boost_tier_2 = 10
    guild_boost_tier_3 = 11
    channel_follow_add = 12
    guild_discovery_disqualified = 14
    guild_discovery_requalified = 15
    guild_discovery_grace_period_initial_warning = 16
    guild_discovery_grace_period_final_warning = 17
    thread_created = 18
    reply = 19
    chat_input_command = 20
    thread_starter_message = 21
    guild_invite_reminder = 22
    context_menu_command = 23
    auto_moderation_action = 24
    role_subscription_purchase = 25
    interaction_premium_upsell = 26
    guild_application_premium_subscription = 32

class GatewayOpcode:
    dispatch = 0
    heartbeat = 1
    identify = 2
    presence_update = 3
    voice_state_update = 4
    resume = 6
    reconnect = 7
    request_guild_members = 8
    invalid_session = 9
    hello = 10
    heartbeat_ack = 11

class NitroPremiumType:
    none = 0
    nitro_classic = 1
    nitro = 2
    nitro_basic = 3

class EmbedType:
    rich = 'rich'
    image = 'image'
    video = 'video'
    gifv = 'gifv'
    article = 'article'
    link = 'link'

class MessageActivityType:
    join = 1
    spectate = 2
    listen = 3
    join_request = 5

class TeamMemberMembershipState:
    invited = 1
    accepted = 2

class OverwriteType:
    role = 0
    member = 1

class GuildForumSortOrderType:
    latest_activity = 0
    creation_date = 1

class GuildForumLayoutType:
    not_set = 0
    list_view = 1
    gallery_view = 2

class VideoQualityMode:
    auto = 1
    full = 2

class ButtonStyle:
    primary = 1
    secondary = 2
    success = 3
    danger = 4
    link = 5

# Flags
class MessageFlags:
    crossposted = 1 << 0
    is_crosspost = 1 << 1
    suppress_embeds = 1 << 2
    source_message_deleted = 1 << 3
    urgent = 1 << 4
    has_thread = 1 << 5
    ephemeral = 1 << 6
    loading = 1 << 7
    failed_to_mention_some_roles_in_thread = 1 << 8

class UserFlags:
    staff = 1 << 0
    partner = 1 << 1
    hypesquad = 1 << 2
    bug_hunter_level_1 = 1 << 3
    hypesquad_online_house_1 = 1 << 6
    hypesquad_online_house_2 = 1 << 7
    hypesquad_online_house_3 = 1 << 8
    premium_early_supporter = 1 << 9
    team_pseudo_user = 1 << 10
    bug_hunter_level_2 = 1 << 14
    verified_bot = 1 << 16
    verified_developer = 1 << 17
    certified_moderator = 1 << 18
    bot_http_interactions = 1 << 19
    active_developer = 1 << 22

class ApplicationFlags:
    gateway_presence = 1 << 12
    gateway_presence_limited = 1 << 13
    gateway_guild_members = 1 << 14
    gateway_guild_members_limited = 1 << 15
    verification_pending_guild_limit = 1 << 16
    embedded = 1 << 17
    gateway_message_content = 1 << 18
    gateway_message_content_limited = 1 << 19
    application_command_badge = 1 << 23

class ChannelFlags:
    pinned = 1 << 1
    require_tag = 1 << 4

# public
class TextInputStyle:
    short = 1
    paragraph = 2
