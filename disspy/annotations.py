from typing import Protocol, Generic, TypeVar, TypeAlias

__all__ = (
    'Strable',
)

T = TypeVar('T')
ST = TypeVar('ST', bound=str)

class Strable(Protocol):
    '''
    (protocol) Strable
    '''
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

class Startswith(str, Generic[ST]):
    '''
    Indicates that this string startswith other string
    
    Using:
    ```
    Startswith['I like disspy'] # F. e., 'I like disspy very much!'
    ```
    '''
    ... # pylint: disable=unnecessary-ellipsis

# Type aliases
Snowflake: TypeAlias = int # f. e., 1234567890987654321
Filename: TypeAlias = str
Url: TypeAlias = Startswith['http']
ProxyUrl: TypeAlias = Url
