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
# Files
import disspy.activity
import disspy.abstract
import disspy.application_commands
import disspy.channel
import disspy.client
import disspy.core
import disspy.embed
import disspy.errors
import disspy.guild
import disspy.user
import disspy.reaction
import disspy.ui
import disspy.thread

# Classes
from disspy.abstract import (
    Channel,
    Message,
    Thread
)
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
    DisDmChannel,
    DisMessage,
    DmMessage,
    MessageDeleteEvent,
    DmMessageDeleteEvent
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
    Snowflake
)
from disspy.embed import (
    DisEmbed,
    DisField,
    DisColor
)
from disspy.guild import DisGuild
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

from disspy.thread import (
    DisNewsThread,
    DisThread,
    DisPrivateThread
)


# Methods for other variables
def _all_generator(alls: list) -> tuple:
    result = []

    for file_all in alls:
        if isinstance(file_all, str):
            result.append(file_all)
        else:
            for element in file_all:
                result.append(element)

    return tuple(result)


# Variables

# Version of disspy
__version__ = "0.6.2.1"

# Link to GitHub repo
__github__ = "https://github.com/itttgg/dispy"

# Link to stable version of package
__latest_version__ = f"https://github.com/itttgg/dispy/releases/tag/{__version__}"

# Description of package
__description__ = "Dispy - package for creating bots in discord."

# Name of package
__packagename__ = "dispy"


# __all__
__alls__: list = [
    disspy.activity.__all__,
    disspy.abstract.__all__,
    disspy.application_commands.__all__,
    disspy.channel.__all__,
    disspy.client.__all__,
    disspy.core.__all__,
    disspy.embed.__all__,
    disspy.errors.__all__,
    disspy.guild.__all__,
    disspy.user.__all__,
    disspy.reaction.__all__,
    disspy.ui.__all__,
    disspy.thread.__all__
]

__all__: tuple = _all_generator(__alls__)
