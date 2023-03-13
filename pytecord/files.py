from typing import TYPE_CHECKING, TypeVar, Generic

if TYPE_CHECKING:
    from pytecord.annotations import Snowflake, Filename, Url, ProxyUrl
    from pytecord.payloads import AttachmentPayload

CT = TypeVar('CT', str, None)

__all__ = (
    'Attachment',
)

class Attachment(Generic[CT]):
    '''
    Attachment (File) object
    
    ### Magic operations
    ---
    
    `int()` -> Attachment id

    `str()` -> Attachment url
     
    ```
    int(attachment)
    str(attachment)
    ```
    '''
    def __init__(self, *_, **data: 'AttachmentPayload') -> None:
        _ = data.get

        self.id: Snowflake = int(_('id')) # pylint: disable=invalid-name
        self.filename: Filename = _('filename')
        self.description: str | None = _('description')
        self.content_type: CT = _('content_type')
        self.size: int = int(_('size'))
        self.url: Url = _('url')
        self.proxy_url: ProxyUrl = _('proxy_url')
        self.height: int | None = _('height')
        self.width: int | None = _('width')
        self.ephemeral: bool = _('ephemeral', False)

    def __int__(self) -> int:
        return self.id
    def __str__(self) -> str:
        return self.url
