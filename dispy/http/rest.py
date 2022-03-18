import requests

class Rest:
    def __init__(self, token):
        self.token = token

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

    def send_message(self, channel_id, post):
        print( requests.post(f'https://discord.com/api/v10/channels/{channel_id}/messages', json = post, headers={'Authorization': f'Bot {self.token}'}).json())
