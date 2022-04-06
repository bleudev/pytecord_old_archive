from .client import DisBot
from .errs import *
from .guild import DisGuild
from .channel import DisChannel
from .embed import DisEmbed, DisField
from .color import DisColor
from .message import DisMessage

"""
    Main information about dispy
    
    :var: __version__ -> Version of dipsy
    :var: __github__ -> Link to github repo
    :var: __packagename__ -> Name of package 
"""

__version__ = "0.2beta"
__github__ = "https://github.com/itttgg/dispy"
__packagename__ = "dispy"


# Types for simpler creating bots
class DisBotEventType:  # Event type for DisBot
    """
    __descripton__
    This class created for simplification adding events to DisBot

    __variables__(It's constants)
    @ON_MESSAGE will be called when new message was created in DisBot.guild.channel
    @ON_READY will be called when bot becomes ready

    __class__
    This is class, not an object
    """
    @property
    def ON_MESSAGE(self):
        return "messagec"

    @property
    def ON_READY(self):
        return "ready"
