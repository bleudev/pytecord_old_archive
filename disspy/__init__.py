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

# Basic imports
from ._typing import TypeOf

from .errs import (
    UserNitroTypeError,
    InternetError,
    MissingPerms,
    InvalidArgument,
    BotEventTypeError,
    BotStatusError,
    ClassTypeError
)

from .core import (
    DisApi,
    DisFlags,
    JsonOutput,
    Showflake
)

from .objects import (
    DisBotStatus,
    DisBotEventType
)

# User imports
from .logger import Logger

from .client import DisBot

from .guild import DisGuild

from .channel import DisChannel

from .embed import (
    DisEmbed,
    DisField,
    DisColor
)

from .message import DisMessage

from .user import DisUser

from .application_commands import (
    ApplicationCommand,
    SlashCommand,
    Context,
    Option,
    OptionType
)

# Version of dipsy (b - beta, a - alpha)
__version__ = "0.1b"

# Minimal python version for using package
__minpythonver__ = "3.8"

# Link to GitHub repo
__github__ = "https://github.com/itttgg/dispy"

# Link to stable version of package
__stablever__ = f"https://github.com/itttgg/dispy/releases/tag/{__version__}"

# Description of package
__description__ = "Dispy - package for creating bots."

# Name of package
__packagename__ = "dispy"

# __all__
__all__ = (
    core.__all__ +
    client.__all__ +
    application_commands.__all__
)
