import aiohttp
import requests


class Rest:
    def __init__(self, token):
        self.token = token
        self._s = aiohttp.ClientSession()

    def _headers(self):
        return {'Authorization': f'Bot {self.token}'}

    def get(self, goal: str, id: int):
        if goal.casefold() == 'guild':
            return requests.get(f'https://discord.com/api/v10/guilds/{str(id)}',
                                headers=self._headers()).json()
        elif goal.casefold() == 'channel':
            return requests.get(f'https://discord.com/api/v10/channels/{str(id)}',
                                headers=self._headers()).json()
        elif goal.casefold() == "user":
            return requests.get(f'https://discord.com/api/v10/users/{str(id)}',
                                headers=self._headers()).json()

    def fetch(self, channel_id, message_id):
        return requests.get(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages/{str(message_id)}',
                            headers=self._headers()).json()

    async def send_message(self, channel_id, post):
        await self._s.post(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages', json=post, headers=self._headers())
