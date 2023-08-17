from abc import ABC as AbstractClass
from abc import abstractmethod as abstract_method
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pytecord.web import GatewayOutput

class BaseDataStreamListener(AbstractClass):
    @abstract_method
    def listen(self, request: 'GatewayOutput'): ...

class Object(AbstractClass):
    @abstract_method
    def __int__(self) -> int: ...
    @abstract_method
    def eval(self) -> dict[str, Any]: ...
