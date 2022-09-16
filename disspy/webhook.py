"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import (
    final,
    Text,
    ClassVar,
    Dict
)

from asyncio import (
    wait,
    sleep
)
from datetime import datetime
from time import mktime
import colorama
from requests import get


from disspy.channel import (
    DisMessage,
    DmMessage,
    MessageDeleteEvent,
    DmMessageDeleteEvent,
    DisChannel,
    DisDmChannel
)
from disspy.reaction import (
    DisEmoji,
    DisReaction,
    DisRemovedReaction
)
from disspy.user import DisUser


class Opcodes:
    """
    Flow Event Opcodes (see Discord Developer Portal docs (topics Gateway)
    """
    DISPATCH: ClassVar[int] = 0
    HEARTBEAT: ClassVar[int] = 1
    IDENTIFY: ClassVar[int] = 2
    PRESENCE_UPDATE: ClassVar[int] = 3
    VOICE_STATE_UPDATE: ClassVar[int] = 4
    RESUME: ClassVar[int] = 6
    RECONNECT: ClassVar[int] = 7
    REQUEST_GUILD_MEMBERS: ClassVar[int] = 8
    INVALID_SESSION: ClassVar[int] = 9
    HELLO: ClassVar[int] = 10
    HEARTBEAT_ACK: ClassVar[int] = 11

    @staticmethod
    def rotated_dict() -> Dict[int, str]:
        """
        Return rotated dict with opcode and this name
        -----
        :return Dict[int, str]: Rotated dict
        """
        return {
            0:  "DISPATCH",
            1:  "HEARTBEAT",
            2:  "IDENTIFY",
            3:  "PRESENCE UPDATE",
            4:  "VOICE STATE UPDATE",
            6:  "RESUME",
            7:  "RECONNECT",
            8:  "REQUEST GUILD MEMBERS",
            9:  "INVALID SESSION",
            10: "HELLO",
            11: "HEARTBEAT ACK"
        }


colorama.init()  # Init Colorama

class _DebugLoggingWebsocket:
    """
    Debug tool for Websocket
    """
    def __new__(cls, *args, **kwargs) -> Text:
        _data: dict = args[0]

        try:
            _send = kwargs["send"]
        except KeyError:
            _send = False

        try:
            _isevent = kwargs["isevent"]
        except KeyError:
            _isevent = False

        try:
            _op = kwargs["op"]
        except KeyError:
            _op = 0

        _datetime = datetime.now()

        _second = _datetime.second if _datetime.second > 9 else f"{_datetime.second}0"

        _date = f"{_datetime.day}/{_datetime.month}/{_datetime.year}"
        _time = f"{_datetime.hour}:{_datetime.minute}:{_second}.{str(_datetime.microsecond)[:2]}"

        _result = f"{colorama.Fore.CYAN}[{_date}: {_time}]{colorama.Fore.RESET} "

        _op_str = Opcodes.rotated_dict()[_op]
        _op_str = _op_str.capitalize()

        _2part = f" | {_op_str}:{colorama.Fore.RESET} {_data}"

        try:
            del _data["d"]["_trace"]
        except KeyError:
            pass
        except TypeError:
            pass

        if _send:
            if _op == 2:
                _data["d"]["token"] = "TOKEN"

            if _op == 11:
                _op_str = "Heartbeat ACK"

            _result += f"{colorama.Fore.GREEN}Sending Request{colorama.Fore.RED}"
        else:
            if _isevent:
                if _op == 11:
                    _op_str = "Heartbeat ACK"

                _result += f"{colorama.Fore.YELLOW}Getting Event{colorama.Fore.RED}"
            else:
                if _op == 11:
                    _op_str = "Heartbeat ACK"

                _result += f"{colorama.Fore.YELLOW}Getting Responce{colorama.Fore.RED}"

        _result += _2part

        return _result


class _DebugLoggingAwaiting:
    def __new__(cls, gateway_event_name, event_name):
        _datetime = datetime.now()

        _second = _datetime.second if _datetime.second > 9 else f"{_datetime.second}0"

        _date = f"{_datetime.day}/{_datetime.month}/{_datetime.year}"
        _time = f"{_datetime.hour}:{_datetime.minute}:{_second}.{str(_datetime.microsecond)[:2]}"

        _result = f"{colorama.Fore.CYAN}[{_date}: {_time}]{colorama.Fore.RESET} "

        _result += f'{colorama.Fore.RED}Awaiting event "{gateway_event_name}": '
        _result += f'{colorama.Fore.YELLOW}{event_name}(){colorama.Fore.RESET}'

        return _result


class _Event:
    """
    Event object with type, session id, data and opcode

    :var type (str): Type of event (For example, "READY")
    :var session (str): Session id of Flow
    :var data (dict): Event's JSON data
    :var opcode (int): Event's OpCode (For example, 0 (Dispatch))
    """

    def __init__(self, json) -> None:
        """
        Init object

        :param json: JSON data
        """
        try:
            self.type = json["t"]
            self.session = json["s"]
            self.data = json["d"]
            self.opcode = json["op"]
            self.json = json
        except TypeError:
            self.type = "ERROR"
            self.session = None
            self.data = {
                "type": "json data is not dict!"
            }
            self.opcode = 0
            self.json = {
                "t": "ERROR",
                "s": None,
                "d": {},
                "op": 0
            }


@final
class DispyWebhook:
    """
    Flow class was created for opening and working with Discord Gateway
    """
    __classname__: str = "Flow"

    def __init__(self, gateway_version: int, token: str, intents: int):

        self.on_channel__id = 0
        self.user_id = "null"
        self.heartbeat_interval = 0

        self.gateway_version: int = gateway_version

        self.intents = intents
        self.activity = None
        self.status = "online"

        # ISes
        self.isrunning = False
        self.isafk = False

        self.token = token
        self._debug = False

        self._headers = {}

        self.websocket = None
        self.session = None
        self.ons = None

    # Event methods
    async def on_channel(self, message: DisMessage):
        """on_channel
        "MESSAGE CREATE" event, but only in one channel

        Args:
            message (DisMessage): Message that was created
        """
        return message.content  # For PyLint

    async def register(self, data):
        """register
        Register user id

        Args:
            data (dict): Data of "READY" event
        """
        self.user_id = data["user"]["id"]

    # Sending/Getting
    async def send_request(self, data, websocket):
        """send_request
        Send json request to Gateway

        Args:
            data (dict): Json data
            ws (Any): Aiohttp websocket

        Returns:
            dict: Your json data
        """
        await websocket.send_json(data)

        if self._debug:
            print(_DebugLoggingWebsocket(data, send=True, isevent=False, op=data["op"]))

        return data

    async def get_responce(self, websocket):
        """get_responce
        Get json output from Gateway

        Args:
            ws (Any): Aiohttp websocket

        Returns:
            dict: Json output
        """
        try:
            j = await websocket.receive_json()
        except TypeError:
            return

        if self._debug:
            try:
                if j["t"]:
                    print(_DebugLoggingWebsocket(j, send=False, isevent=True, op=j["op"]))
                else:
                    print(_DebugLoggingWebsocket(j, send=False, isevent=False, op=j["op"]))
            except KeyError:
                print(_DebugLoggingWebsocket(j, send=False, isevent=False, op=j["op"]))

        return j

    # Runners
    async def run(self, ons, status, debug, act, session):
        """run
        Run Flow (Gateway)

        Args:
            ons (dict): Dict with _type_: _func_ model for awaiting this events
            status (str): Status of bot
            debug (bool): Debug id enabled?
            act (dict): Activity of bot
        """
        self._debug = debug
        self.status = status
        self.activity = act
        self.ons = ons

        # Registering events
        if ons["channel"][0] is not None:
            self.on_channel = ons["channel"][0]
            self.on_channel__id = ons["channel"][1]

        # Other
        self.isrunning = True
        self.isafk = False

        self.session = session

        await self._runner()

    async def _runner(self):
        async with self.session.ws_connect(
            f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json") as websocket:
            self.websocket = websocket

            j = await self.get_responce(websocket)

            interval = j["d"]["heartbeat_interval"]


            await self.send_request({"op": 2, "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "disspy",
                    "$device": "disspy"
                },
                "presence": {
                    "since": mktime(datetime.now().timetuple()) * 1000,
                    "afk": self.isafk,
                    "status": self.status,
                    "activities": [self.activity]
                }
            }}, websocket)

            self.isrunning = True

            await wait(
                fs=[self.heartbeat(websocket, interval / 1000),
                    self._events_checker(websocket)])  # Run Gateway client

    async def heartbeat(self, websocket, interval):
        """heartbeat
        Function with sending heartbeating to Gateway

        Args:
            websocket (Any): Aiohttp websocket
            interval (int): Heartbeat interval
        """
        while True:
            await self.send_request({"op": 1, "d": None, "t": None}, websocket)

            await sleep(interval)

    async def _events_checker(self, websocket):
        while True:
            event_json = await self.get_responce(websocket)
            event = _Event(event_json)

            try:
                if event.type == "READY":
                    await self.register(event.data)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "register"))

                    await self.ons["register2"](event.data)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_register2"))

                    await self.ons["register"](event.data)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_register"))

                    await self.ons["ready"]()

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_ready"))

                elif event.type == "MESSAGE_CREATE":
                    _u: str = f"https://discord.com/api/v10/channels/{event.data['channel_id']}"

                    if not event.data["author"]["id"] == self.user_id:
                        async with self.session.get(_u) as data:
                            j = await data.json()

                            if j["type"] == 0:
                                _m = DisMessage(event.data, self.token, self.session)

                                if int(event.data["channel_id"]) == int(self.on_channel__id):
                                    await self.on_channel(_m)

                                    if self._debug:
                                        print(_DebugLoggingAwaiting(event.type, "on_channel"))


                                await self.ons["messagec"](_m)

                                if self._debug:
                                    print(_DebugLoggingAwaiting(event.type, "on_messagec"))
                            elif j["type"] == 1:
                                _m = DmMessage(event.data, self.token, self.session)

                                await self.ons["dmessagec"](_m)

                                if self._debug:
                                    print(_DebugLoggingAwaiting(event.type, "on_dmessagec"))

                elif event.type == "MESSAGE_UPDATE":
                    _u: str = f"https://discord.com/api/v10/channels/{event.data['channel_id']}"

                    if not event.data["author"]["id"] == self.user_id:
                        async with self.session.get(_u) as data:
                            j = await data.json()

                            if j["type"] == 0:
                                _m = DisMessage(event.data, self.token, self.session)

                                await self.ons["messageu"](_m)

                                if self._debug:
                                    print(_DebugLoggingAwaiting(event.type, "on_messageu"))
                            elif j["type"] == 1:
                                _m = DmMessage(event.data, self.token, self.session)

                                await self.ons["dmessageu"](_m)

                                if self._debug:
                                    print(_DebugLoggingAwaiting(event.type, "on_dmessageu"))

                elif event.type == "MESSAGE_DELETE":
                    _u = f"https://discord.com/api/v10/channels/{event.data['channel_id']}"

                    async with self.session.get(_u) as data:
                        j = await data.json()

                        if j["type"] == 0:
                            _e = MessageDeleteEvent(event.data, self.token)

                            await self.ons["messaged"](_e)

                            if self._debug:
                                print(_DebugLoggingAwaiting(event.type, "on_messaged"))
                        elif j["type"] == 1:
                            _e = DmMessageDeleteEvent(event.data, self.token)

                            await self.ons["dmessaged"](_e)

                            if self._debug:
                                print(_DebugLoggingAwaiting(event.type, "on_dmessaged"))

                elif event.type == "INTERACTION_CREATE":
                    if event.data["type"] == 2:  # Application Commands
                        await self.ons["interaction"](event.data)

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_interaction"))
                    if event.data["type"] == 3 or event.data["type"] == 4:  # Components
                        await self.ons["components"](event.data)

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_components"))

                    if event.data["type"] == 5:  # Modal Sumbit
                        await self.ons["modalsumbit"](event.data)

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_modalsumbit"))

                elif event.type == "MESSAGE_REACTION_ADD":
                    _u = DisUser(event.data["member"]["user"], self.token)
                    _m_id = int(event.data["message_id"])
                    _c_id = int(event.data["channel_id"])
                    _g_id = int(event.data["guild_id"])

                    _e_json = event.data["emoji"]

                    if _e_json["id"] is None:
                        _e = DisEmoji(unicode=_e_json["name"])
                    else:
                        _e = DisEmoji(name=_e_json["name"], emoji_id=int(_e_json["id"]))

                    _r = DisReaction(_u, _m_id, _c_id, _g_id, _e, self.token)

                    await self.ons["reaction"](_r)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_reaction"))

                elif event.type == "MESSAGE_REACTION_REMOVE":
                    _m_id = int(event.data["message_id"])
                    _c_id = int(event.data["channel_id"])
                    _g_id = int(event.data["guild_id"])

                    _e_json = event.data["emoji"]

                    if _e_json["id"] is None:
                        _e = DisEmoji(unicode=_e_json["name"])
                    else:
                        _e = DisEmoji(name=_e_json["name"], emoji_id=int(_e_json["id"]))

                    _r = DisRemovedReaction(_m_id, _c_id, _g_id, _e, self.token)

                    await self.ons["reactionr"](_r)

                    if self._debug:
                        print(_DebugLoggingAwaiting(event.type, "on_reactionr"))

                elif event.type == "TYPING_START":
                    try:
                        if event.data["guild_id"]:
                            _u: DisUser = DisUser(event.data["member"]["user"], self.token)
                            _c: DisChannel = DisChannel(event.data["channel_id"], self.token)

                            await self.ons["typing"](_u, _c)

                            if self._debug:
                                print(_DebugLoggingAwaiting(event.type, "on_typing"))
                        else:
                            _u_id = event.data["user_id"]

                            _url = f'https://discord.com/api/v10/users/{str(_u_id)}'

                            _u_json = get(url=_url, headers=self._headers).json()

                            _u: DisUser = DisUser(_u_json, self.token)
                            _c: DisDmChannel = DisDmChannel(event.data["channel_id"], self.token)

                            await self.ons["dm_typing"](_u, _c)

                            if self._debug:
                                print(_DebugLoggingAwaiting(event.type, "on_dm_typing"))
                    except KeyError:
                        _u_id = event.data["user_id"]

                        _url = f'https://discord.com/api/v10/users/{str(_u_id)}'

                        _u_json = get(url=_url, headers=self._headers).json()

                        _u: DisUser = DisUser(_u_json, self.token)
                        _c: DisDmChannel = DisDmChannel(event.data["channel_id"], self.token)

                        await self.ons["dm_typing"](_u, _c)

                        if self._debug:
                            print(_DebugLoggingAwaiting(event.type, "on_dm_typing"))
            except TypeError:
                pass
            except KeyError:
                pass

            await sleep(0.5)

    async def disconnecter(self):
        """disconnecter
        Disconnect from Gateway
        """
        await self.websocket.close()
