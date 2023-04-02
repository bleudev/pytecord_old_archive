from pytecord.hook import Hook


class Connection:
    def __init__(self, *, token: str, **options) -> None:
        self._run_token = token
        self._hook = Hook(token=token, **options)
        self._headers = {
            "Authorization": f"Bot {token}",
            "content-type": "application/json",
        }
        self._listener = None
    
    async def run(self, listener, app_client, **options):
        self._listener = listener
        await self._hook.run(options['session'], self._listener, app_client, **options)
