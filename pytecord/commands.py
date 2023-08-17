from typing import Any, Literal
from .interfaces import Object
from .utils import MessagePayload, apost, get_snowflake
from .enums import InteractionCallbackType


class AppllicationCommandOption:
    def __init__(self, type: int, name: str, description: str = '...', required: bool = False, data: dict[str, Any] = None) -> None:
        if data:
            type = data['type']
            name = data['name']
            description = data.get('description', '...')
            required = data.get('required', False)
        self.type = type
        self.name = name
        self.name_localizations = ...
        self.description = description
        self.description_localizations = ...
        self.required = required
        self.choices = ...
        self.options = ...
        self.channel_types = ...
        self.min_value = ...
        self.max_value = ...
        self.min_length = ...
        self.max_length = ...
        self.autocomplete = ...
    
    def eval(self) -> dict[str, Any]:
        return {
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'required': self.required
        }


class AppllicationCommand:
    def __init__(self, name: str, description: str = '...', options: list[AppllicationCommandOption] = [], type: Literal[1, 2, 3] = 1, data: dict[str, Any] = None, token: str = None) -> None:
        if data:
            type = data.get('type', 1)
            name = data['name']
            description = data.get('description', '...')
            options = [AppllicationCommandOption(data=i) for i in data.get('options', [])]
        self.id: int = int(data.get('id')) if data else None
        self.type: int = type
        self.application_id: int = int(data.get('application_id')) if data else None
        self.name = name
        self.name_localizations = ...
        self.description = description
        self.description_localizations = ...
        self.options: list[AppllicationCommandOption] = options
        self.default_member_permissions = ...
        self.dm_permission = ...
        self.nsfw = ...
        self.version: int = int(data.get('version')) if data else None

        self.__guild_id = int(data.get('guild_id')) if data else None
        self.__token = token if data else None

    def eval(self) -> dict[str, Any]:
        return {
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'options': [i.eval() for i in self.options]
        }


class Interaction(Object):
    def __init__(self, data: dict[str, Any], token: str) -> None:
        self.id = get_snowflake(data.get('id'))
        self.token = data.get('token')
        self.type = data.get('type')

        self.__token = token
        self.__data = data
    
    async def message(self, content: str, ephemeral: bool = True):
        message = MessagePayload(content)
        message['flags'] = 1 << 6 if ephemeral else 0

        payload = {
            'type': InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': message.json
        }

        await apost(f'/interactions/{self.id}/{self.token}/callback', self.__token, data=payload)
    
    def __int__(self) -> int:
        return self.id
    
    def eval(self) -> dict[str, Any]:
        return self.__data
