import json, threading, websocket, time


class Gateway:
    def __init__(self, gateway_version: int, token: str, intents: int, activity: dict, status: str):
        # Setting up connecting to Gateway
        self.gateway_version: int = gateway_version
        self.ws = websocket.WebSocket()
        self.intents = intents
        self.activity = activity
        self.status = status
        self.token = token

        # Connecting to Gateway
        self.ws.connect(f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json")

        # Parsing Opcode 10 Hello to Heartbeat Interval
        self.heartbeat_interval = self.get_responce()["d"]["heartbeat_interval"]

        # Setting up Opcode 1 Heartbeat
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.heartbeat_thread.start()

        # Sending Opcode 2 Identify
        self.send_request({"op": 2, "d": {"token": self.token,
                                          "properties": {"$os": "linux", "$browser": "dispy", "$device": "dispy"},
                                          "presence": {"activities": [activity],
                                                       "status": self.status, "since": 91879201, "afk": False},
                                          "intents": self.intents}})

    def send_request(self, json_data):
        self.ws.send(json.dumps(json_data))

    def get_responce(self):
        responce = self.ws.recv()
        print(responce)
        return json.loads(responce)

    def heartbeat(self):
        while True:
            self.send_request({"op": 1, "d": "null"})
            self.get_responce()
            time.sleep(self.heartbeat_interval / 1000)


class GatewayClient:
    def __init__(self, gateway_version: int, token: str, intents: int, activity: dict, status: str):
        self._gateway = Gateway(gateway_version, token, intents, activity, status)

    def get_event(self):
        return self._gateway.get_responce()

GatewayClient(10, "", 512, {"name": "Test"}, "online")
