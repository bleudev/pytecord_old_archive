import dispy
import dispy.http.rest


class DisMessage:
    def __init__(self, data, rest: dispy.http.rest.Rest):
        self.id = data["id"]
        self._rest = rest
        self.channel = dispy.DisChannel(self._rest.get("channel", data["channel_id"]), rest)
        self.guild = dispy.DisGuild(self._rest.get("guild", data["guild_id"]), rest)
