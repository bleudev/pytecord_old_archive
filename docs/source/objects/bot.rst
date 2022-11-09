Bot
###

Client
******

::

    class Client(token: str,
                 flags: Optional[TypeOf(Flags)], debug: Optional[bool] = False,
                 activity: Optional[Union[Activity, dict]])

``token`` -> Token of bot from Discord Developer Portal

``status`` -> Key of `DisBotStatus`_ object. Bot status in Discord (for example, "online")

.. note::
    Default is ``DisBotStatus.ONLINE``

``flags`` -> Key of Flags. Special privellegions for bot (for example, Flags.messages() for on_message() events, or Flags.reactions() for on_reaction() events)

.. note::
    Default is ``Flags.default()``

``debug`` -> Enable debug logs in console?

.. note::
    Default is ``False``

``activity`` -> Bot activity in Discord (For example, ``playing in Disspy``)

.. note::
    Default is ``None``

add_event()
===========

::

    def add_event(event_type: str, func: Callable) -> None

Registering events with event type and function

Example::

    async def on_ready():
        print("I'm ready!")
    
    bot.add_event("ready", on_ready)

Params:
    ``event_type: str`` -> Key of `EventType`_

    ``func: Callable`` -> `Callable <https://docs.python.org/3/library/typing.html#callable>`_ argument. Function for event

Returns:
    ``None``

@on_ready()
===========

::

    @on_ready() -> Wrapper

Register on_ready() event

Example::

    @bot.on_ready()
    async def on_ready():
        print(f"Logged by {bot.user.fullname}")

Params:
    ``None``

Returns:
    ``Wrapper``

@on_message()
=============

::

    @on_message(event_type: str) -> Wrapper

Register on_message() events

Example::

    @bot.on_message("create")
    async def on_messagec(message: disspy.Message):
        await message.channel.send(f"Channel id: {message.channel.id}")

Params:
    ``event_type: str`` -> Key of ["create", "update", "delete"] list

Returns:
    ``Wrapper``

@on_dm_message()
================

::

    @on_dm_message(event_type: str) -> Wrapper

Register on_dmessage() events

Example::

    @bot.on_dm_message("update")
        async def on_dmessageu(message: disspy.Message):
            await message.channel.send("Dota 2 - 👎🏼")

Params:
    ``event_type: str`` -> Key of ["create", "update", "delete"] list

Returns:
    ``Wrapper``

@on_channel()
=============

::

    @on_channel(channel_id: int) -> Wrapper

Register on_channel() event (on_messagec() event, but in one channel)

Example::

    @bot.on_channel(955869165162479648)
    async def on_channel(message: disspy.Message):
        await message.reply("Hi")

Params:
    ``channel_id: int`` -> Channel id for event

Returns:
    ``Wrapper``

@command()
==========

.. warning::
    For application commands your bot needs have ``application.commands`` scope

::

    @command(*name: str) -> Union[Wrapper, None]

Create `Slash command. <application_commands.html#slash-commands>`_


Example::

    @bot.command()
    async def test(ctx: disspy.Context):
        await ctx.send("Test!")

Params:
    ``*name: str`` -> Name of command

    .. note::
        Default is ``None``

Args for event:
    ``ctx`` -> `Context <application_commands.html#context>`_ object. Command context

Returns:
    ``Union[Wrapper, None]`` -> Wrapper if application_id != 0 else None and error

More info in `this page <application_commands.html#slash-commands>`_

@context_menu()
===============

.. warning::
    For application commands your bot needs have ``application.commands`` scope

::

    @context_menu(*name: str) -> Wrapper

Create `User or Message command. <application_commands.html#user-commands>`_

Example::

    @bot.context_menu()  # Example user command
    async def info(ctx: Context, user: User):
        await ctx.send(f"Fullname: {user.fullname}")
    
    @bot.context_menu()  # Example message command
    async def info_again(ctx: Context, message: Message):
        await ctx.send(message.content)

Params:
    ``name: str`` -> Name of user command

Args for event:
    ``ctx`` -> `Context <application_commands.html#context>`_ object. Command context

    ``user or message`` -> Resolved user or message

Returns:
    ``Wrapper``

run()
=====

::

    def run(status: Optional[DisBotStatus | str], activity: Optional[Activity | dict]) -> None

Run the bot in Discord Gateway

Example::

    bot.run(DisBotStatus.DND)

Params:
    ``status`` -> Key of `DisBotStatus`_

    ``activity`` -> Activity object. Discord activity in profile

Returns:
    ``None``

disconnect()
============

::

    async def disconnect() -> None

Disconnect from Discord Gateway

Example::

    await bot.disconnect()

Returns:
    ``None``

close()
=======

::

    async def close() -> None

Alternative of `disconnect()`_ method

send()
======

::

    async def send(channel_id: int, content: Optional[str],
                   embeds: Optional[List[Embed]])

Send message to channel by id

Example::

    await bot.send(1001044473331060818, "I'm a bot created with disspy :)")

Params:
    ``channel_id`` -> Channel id where needs to send message

    ``content`` -> Message content

    ``embeds`` -> Message embeds

Returns:
    ``None``

get_channel()
=============

::

    def get_channel(channel_id: int) -> Channel

Get channel by id

Example::

    ch = bot.get_channel(1001044473331060818)
    await ch.send("Hi?")

Params:
    ``channel_id`` -> Channel id. ``int`` type

Returns:
    ``Channel``

get_guild()
===========

::

    def get_guild(guild_id: int) -> Guild

Get guild by id

Example::

    gl = bot.get_guild(955868993175035934)

Params:
    ``guild_id`` -> Guild id. ``int`` type

Returns:
    ``Guild``


change_activity()
=================

::

    async def change_activity(activity: Activity | dict) -> None

Change activity in bot profile

Example::

    await bot.change_activity(Activity("I'm working", ActivityType.WATCHING))

Params:
    ``activity`` -> Activity object. Bot activity

Returns:
    ``None``

DisBotStatus
************

.. image:: images/bot_statuses.png

::

    class DisBotStatus

Class with constants representes Discord bot statues

Variables:
    * ``ONLINE`` -> Online status (1st status on image)
    * ``DND`` -> Do not disturb status (3rd status on image)
    * ``INVISIBLE`` -> Invisible status (5th status on image)
    * ``IDLE`` -> Idle status (2nd status on image)

EventType
***************

All events in disspy

Variables:
    * ``ON_MESSAGEC`` -> On message create
    * ``ON_MESSAGEU`` -> On message update
    * ``ON_MESSAGED`` -> On message delete
    * ``ON_DMESSAGEC`` -> On message create in DM channel
    * ``ON_DMESSAGEU`` -> On message update in DM channel
    * ``ON_DMESSAGED`` -> On message delete in DM channel
    * ``ON_READY`` -> On ready
    * ``ON_CLOSE`` -> On close
    * ``ON_REACTION`` -> On reaction add
    * ``ON_REACTIONR`` -> On reaction remove
    * ``ON_TYPING`` -> On typing start
    * ``ON_DM_TYPING`` -> On typing start in DM channel

ON_MESSAGEC
===========

Represention of Gateway "MESSAGE_CREATE" event

Args for event:
    message -> `Message <message.html#dismessage>`_ object. Message that was created

ON_MESSAGEU
===========

Represention of Gateway "MESSAGE_UPDATE" event

Args for event:
    message -> `Message <message.html#dismessage>`_ object. Message that was updated

ON_MESSAGED
===========

Represention of Gateway "MESSAGE_DELETE" event

Args for event:
    event -> `Raw message <message.html#rawmessage>`_ object. Message deleting event

ON_DMESSAGEC
============

Represention of Gateway "MESSAGE_CREATE" event only in DM channel

Args for event:
    message -> `Message <message.html#dmmessage>`_ object. Message that was created

ON_DMESSAGEU
============

Represention of Gateway "MESSAGE_UPDATE" event only in DM channel

Args for event:
    message -> `Message <message.html#dmmessage>`_ object. Message that was updated

ON_DMESSAGED
============

Represention of Gateway "MESSAGE_DELETE" event only in DM channel

Args for event:
    event -> `Raw message <message.html#rawmessage>`_ object. Message deleting event

ON_READY
========

Represention of Gateway "READY" event

Args for event:
    ``None``

ON_CLOSE
========

Will be called when calling ``Client.__del__`` function

Args for event:
    ``None``

ON_REACTION
===========

Represention of Gateway "REACTION_ADD" event

Args for event:
    reaction: Reaction object. Reaction that was added

ON_REACTIONR
============

Represention of Gateway "REACTION_REMOVE" event

Args for event:
    reaction: Reaction object. Reaction that was removed

ON_TYPING
=========

Represention of Gateway "TYPING_START" event

Args for event:
    ``user``: User object. User who started typing

    ``channel``: Channel object. Channel where typing was started

ON_DM_TYPING
============

Represention of Gateway "TYPING_START" event only in DM channel

Args for event:
    ``user``: User object. User who started typing

    ``channel``: Channel object. Channel where typing was started
