"""
    Info
    --------

"""

class DisGuild:
    """
    Info
    --------
    Class for manage Guilds in discord
    Atributies
    --------
    :var id: ID of guild

    System atributies
    --------
    :var _api: Api client with Rest and Gatewat client.
    """
    def __init__(self, id, api):
        """
        init object

        :param id: Id for json data getter
        :param api: Api Client for uptade guild and getting data of guild
        """
        self._api = api
        self.id = id

        _data = self._api.get_guild_json(id)

        self.json = _data
