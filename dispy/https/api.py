from . import Gateway, Rest
from .. import DisMessage, DisUser, DisChannel, DisGuild


class DisApi:
    def __init__(self, token):
        self.token = token

        self._g = None
        self._r = Rest(self.token)

    async def _on_ready(self):
        return

    def run(self, gateway_version: int, intents: int, status):
        self._g = Gateway(gateway_version, self.token, intents, {}, status, self._on_ready, self._on_message, self._register)
        self._g.run()

    async def _register(self, d):
        self.user: DisUser = self.get_user(d["user"]["id"], False)

    async def _on_message(self, message: DisMessage):
        return

    def get_user(self, id: int, premium_gets):
        return DisUser(id, self._r, premium_gets)

    def get_channel(self, id: int):
        return DisChannel(self._r.get('channel', id), self._r)

    def get_guild(self, id: int):
        return DisGuild(self._r.get('guild', id), self._r)
