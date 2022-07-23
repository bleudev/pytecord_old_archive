"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Imports
from disspy.activity import (
    Activity,
    ActivityType
)
from disspy.application_commands import (
    ApplicationCommandType,
    ApplicationCommand,
    SlashCommand,
    UserCommand,
    MessageCommand,
    Context,
    Option,
    OptionType,
    OptionArgs
)
from disspy.channel import (
    DisChannel,
    DisDmChannel
)
from disspy.client import (
    DisBot,
    DisBotStatus,
    DisBotEventType
)
from disspy.core import (
    DisApi,
    DisFlags,
    JsonOutput,
    Showflake
)
from disspy.embed import (
    DisEmbed,
    DisField,
    DisColor
)
from disspy.errors import (
    UserNitroTypeError,
    InternetError,
    MissingPerms,
    InvalidArgument,
    BotEventTypeError,
    BotStatusError,
    ClassTypeError,
    BotApplicationIdInvalid,
    BotEventVisibleError,
    ApplicationIdIsNone,
    Unauthorized
)
from disspy.guild import DisGuild
from disspy.logger import Logger
from disspy.message import (
    DisMessage,
    DmMessage,
    MessageDeleteEvent,
    DmMessageDeleteEvent
)
from disspy.user import DisUser
from disspy.reaction import (
    DisEmoji,
    DisOwnReaction,
    DisReaction,
    DisRemovedReaction
)
from disspy.ui import (
    Component,
    ActionRow,
    Button,
    ButtonStyle,
    TextInput,
    SelectMenu,
    SelectMenuOption
)


# Methods for other varibles
def _all_generator(alls: list[tuple]) -> tuple:
    r = []

    for t in alls:
        if isinstance(t, str):
            r.append(t)
        else:
            for e in t:
                r.append(e)

    return tuple(r)


# Version of dipsy (b - beta, a - alpha)
__version__ = "0.3"

# Minimal python version for using package
__pythonversion__ = "3.8"

# Link to GitHub repo
__github__ = "https://github.com/itttgg/dispy"

# Link to stable version of package
__stableversion__ = f"https://github.com/itttgg/dispy/releases/tag/{__version__}"

# Description of package
__description__ = "Dispy - package for creating bots in discord."

# Name of package
__packagename__ = "dispy"

import disspy._typing, disspy.activity,\
       disspy.application_commands, disspy.channel,\
       disspy.client, disspy.core, disspy.embed,\
       disspy.errors, disspy.guild, disspy.logger,\
       disspy.message, disspy.user, disspy.reaction

# __all__
__alls__: list[tuple] = [
    disspy._typing.__all__,
    disspy.activity.__all__,
    disspy.application_commands.__all__,
    disspy.channel.__all__,
    disspy.client.__all__,
    disspy.core.__all__,
    disspy.embed.__all__,
    disspy.errors.__all__,
    disspy.guild.__all__,
    disspy.logger.__all__,
    disspy.message.__all__,
    disspy.user.__all__,
    disspy.reaction.__all__
]

__all__: tuple = _all_generator(__alls__)


# Info
def __info__():
    from time import sleep as tsleep

    print(
        "Dispy is package for creating bots in Discord. This use aiohttp, requests and other packages for using discord API")

    tsleep(1)  # 1-second sleep

    print("""
For staring you must create DisBot object:
                    
    import disspy
        
    bot = disspy.DisBot("YOUR_TOKEN")
        
    bot.run()
        
run() method use for running bot Gateway client and starting bot work.
    """)

    del tsleep  # Delete import
