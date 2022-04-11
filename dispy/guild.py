from dispy.https import Rest


class DisGuild:
    """
    Class for manage Guilds in discord

    :propertes:
    id - id of guild
    """
    def __init__(self, data, rest: Rest):
        """
        init object

        :param data: dict - Json data for guild
        :param rest: http.Rest - Rest Client for uptade guild
        """
        self.json = data
        self._rest = rest

    @property
    def id(self):
        """
        id of guild

        :return int:
        """
        return self.json["id"]
