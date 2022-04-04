import dispy.http.rest


class DisGuild:
    """
    Class for manage Guilds in discord

    :propertes:
    id - id of guild
    """
    def __init__(self, data, rest: dispy.http.rest.Rest):
        self.json = data
        self._rest = rest

    @property
    def id(self):
        return self.json["id"]
