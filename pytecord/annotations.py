from typing import Protocol, Generic, TypeVar, TypeAlias, Any

__all__ = (
    'Strable',
)

T = TypeVar('T', type, tuple[str, ...])
ST = TypeVar('ST', bound=str)

class Strable(Protocol): # pylint: disable=too-few-public-methods
    '''
    (protocol) Strable
    '''
    def __str__(self) -> str:
        ...

class Subclass(Generic[T]): # pylint: disable=too-few-public-methods
    '''
    Only subclass of given class

    Using:
    ```
    Subclass[Class]
    ```
    '''
    ... # pylint: disable=unnecessary-ellipsis

class Value(Generic[T]): # pylint: disable=too-few-public-methods
    '''
    The definite value of the any variable
    (likes Literal but may a variable value)
    
    Using:
    ```
    Value['hello']
    Value['hello', 'world', 123] # 'hello' or 'world' or 123
    ```
    '''
    ... # pylint: disable=unnecessary-ellipsis

class Startswith(str, Generic[ST]):
    '''
    Indicates that this string startswith other string
    
    Using:
    ```
    Startswith['I like pytecord'] # F. e., 'I like pytecord very much!'
    ```
    '''
    ... # pylint: disable=unnecessary-ellipsis

# Type aliases
Snowflake: TypeAlias = int | str # f. e., 1234567890987654321
Filename: TypeAlias = str
Url: TypeAlias = Startswith['http']
ProxyUrl: TypeAlias = Url
