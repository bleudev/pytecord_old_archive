from typing import Literal, Any
from datetime import datetime
from time import mktime
from asyncio import create_task

from .web import BaseWebhook, GatewayRequest

class Activity:
    def __init__(self, name: str, type: Literal[0, 1, 2, 3, 4, 5] = 0, state: str = None, *, url: str = None, data: dict[str, Any] = None) -> None:
        if data:
            self.name = data.get('name')
            self.type = data.get('type')
            self.url = data.get('url')
            self.created_at = data.get('created_at')
            self.timestamps = data.get('timestamps')
            self.application_id = data.get('application_id')
            self.details = data.get('details')
            self.state = data.get('state')
            self.emoji = data.get('emoji')
            self.party = data.get('party')
            self.assets = data.get('assets')
            self.secrets = data.get('secrets')
            self.instance = data.get('instance')
            self.flags = data.get('flags')
            self.buttons = data.get('buttons')
        else:
            self.name = name
            self.type = type
            self.url = url
            self.state = state

    def eval(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'type': self.type,
            'url': self.url,
            'state': self.state
        }


class Presence:
    def __init__(self, activities: list[Activity], status: Literal['online', 'dnd', 'idle', 'invisible', 'offline'] = 'online', afk: bool = False) -> None:
        self.since: int = int(mktime(datetime.now().timetuple()) * 1000)
        self.activities = activities
        self.status = status
        self.afk = afk
    
    def register(self, webhook: BaseWebhook):
        if webhook.stream.running:
            create_task(webhook.stream.send_request(GatewayRequest(3, {
                'since': self.since,
                'activities': [i.eval() for i in self.activities],
                'status': self.status,
                'afk': self.afk
            })))
