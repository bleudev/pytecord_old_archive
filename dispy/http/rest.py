import aiohttp
import requests


class Rest:
    def __init__(self, token):
        self.token = token

    def _headers(self):
        return {'Authorization': f'Bot {self.token}'}

    def _gateway(self):
        return requests.get("https://discord.com/api/v10/gateway").json()

    def get(self, goal: str, id: int):
        if goal.casefold() == 'guild':
            return requests.get(f'https://discord.com/api/v10/guilds/{str(id)}',
                                headers={'Authorization': f'Bot {self.token}'}).json()
        elif goal.casefold() == 'channel':
            return requests.get(f'https://discord.com/api/v10/channels/{str(id)}',
                                headers={'Authorization': f'Bot {self.token}'}).json()

    def fetch(self, channel_id, message_id):
        return requests.get(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages/{str(message_id)}',
                            headers={'Authorization': f'Bot {self.token}'}).json()

    async def send_message(self, channel_id, post):
        async with aiohttp.ClientSession() as session:
            await session.post(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages', json=post, headers={'Authorization': f'Bot {self.token}'})
