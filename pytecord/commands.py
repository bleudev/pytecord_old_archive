from typing import Any
from .interfaces import Object
import json
from .utils import MessagePayload, apost, get_snowflake
from .enums import InteractionCallbackType

class ApllicationCommand:
    def __init__(self, name: str, description: str = '...', data: dict[str, Any] = None) -> None:
        if data:
            name = data['name']
            description = data['description']
        self.name = name
        self.description = description

    def eval(self) -> dict[str, Any]:
        return json.dumps({
            'name': self.name,
            'description': self.description
        })


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

        payload = json.dumps({
            'type': InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': message.json
        })

        await apost(f'/interactions/{self.id}/{self.token}/callback', self.__token, data=payload)
    
    def __int__(self) -> int:
        return self.id
    
    def eval(self) -> dict[str, Any]:
        return self.__data
