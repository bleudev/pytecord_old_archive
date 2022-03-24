from .client import DisBot
from .err import *
from .guild import DisGuild
from .channel import DisChannel
from .embed import DisEmbed, DisField
from .color import DisColor

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
    @property
    def ON_MESSAGE(self):
        return "messagecreate"

    @property
    def ON_READY(self):
        return "ready"
