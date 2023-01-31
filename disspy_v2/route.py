api_version = 10

class Route:
    def __init__(self, endpoint: str = '') -> None:
        mainpoint = f'https://discord.com/api/v{api_version}'

        self._endpoint = endpoint
        self.url = mainpoint + endpoint
    def __str__(self) -> str:
        return self.url
    
    def __truediv__(self, other):
        if isinstance(other, Route):
            return Route(self._endpoint + other._endpoint)
        return Route(self._endpoint + str(other))
