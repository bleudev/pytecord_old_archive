from abc import ABC as AbstractClass
from abc import abstractmethod as abstract_method

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pytecord.web import GatewayOutput

class BaseDataStreamListener(AbstractClass):
    @abstract_method
    def listen(self, request: 'GatewayOutput'): ...
