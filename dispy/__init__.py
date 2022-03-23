from .client import *
from .err import *
from .guild import *
from .channel import *
from .types import *
from .embed import *
from .color import *

__version__ = "0.1beta"
__github__ = "https://github.com/itttgg/dispy"
__packagename__ = "dispy"


# Types for simpler creating bots
class DisBotEventType:  # Event type for DisBot
    """
    __descripton__
    This class created for simplification adding events to DisBot

    __variables__(It's constants)
    @ON_MESSAGE will be called when new message was created in DisBot.guild.channels
    @ON_READY will be called when bot becomes ready

    __class__
    This is class, not an object
    """
    ON_MESSAGE = "messagecreate"
    ON_READY = "ready"
