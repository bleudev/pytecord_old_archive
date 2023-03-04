from typing import Protocol, Generic, TypeVar

__all__ = (
    'Strable',
)

T = TypeVar('T', bound=type)

class Strable(Protocol):
    def __str__(self) -> str:
        ...

class Subclass(Generic[T]):
    '''
    Only subclass of given class

    Example using:
    ```
    Subclass[Class]
    ```
    '''
    ... # pylint: disable=unnecessary-ellipsis
