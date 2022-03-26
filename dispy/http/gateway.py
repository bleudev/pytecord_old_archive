import websocket
import json
import threading
import time

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    responce = ws.recv()
    if responce:
        return json.loads(responce)

def heartbeat(interval, ws):
    print("Heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 10,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
event = recieve_json_response(ws)

heartbeat_inverval = event["d"]["heartbeat_interval"] / 1000
t = threading.Thread(target=heartbeat, args=[heartbeat_inverval, ws])

t.start()

token = "TOKEN"
payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}

send_json_request(ws, payload)

while True:
    event = recieve_json_response(ws)

    try:
        print(f"{event['d']['author']['username']}: {event['d']['content']}")
        op_code = event['op']

        if op_code == 11:
            print("Heartbeat received")
    except:
        pass
