import requests
import dispy.http.rest


class Gateway:
    def __init__(self, _rest: dispy.http.rest.Rest):
        self._rest = _rest
        self._link = requests.get("https://discord.com/api/v10/gateway", headers=self._rest._headers())
