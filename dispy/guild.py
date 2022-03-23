import dispy.http.rest

class DisGuild:
    def __init__(self, data, rest: dispy.http.rest.Rest):
        self.id = data["id"]
        self._rest = rest
