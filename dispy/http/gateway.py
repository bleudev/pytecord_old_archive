import websocket


class Gateway:
    def __init__(self, token, rest):
        self._token = token
        self._rest = rest
        self._ws = websocket.WebSocket()

        self._ws.connect(self._rest._gateway())

    def get_event(self, ws: websocket.WebSocket):
        return
