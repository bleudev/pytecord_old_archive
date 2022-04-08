import dispy.http.rest

class _UserBase:
    def __init__(self, id, rest: dispy.http.rest.Rest):
        self.id = id
        self._rest = rest

        # Data
        _data = self._rest.get("user", self.id)

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}{self.discriminator}"

        self.isbot: bool = _data["bot"]
        self.issystem: bool = _data["system"]
        self.isverified: bool = _data["verified"]

    def uptade(self) -> None:
        _data = self._rest.get("user", self.id)

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}{self.discriminator}"

        self.isbot: bool = _data["bot"]
        self.issystem: bool = _data["system"]
        self.isverified: bool = _data["verified"]  # May be ""
        self.email: bool = _data["email"]  # May be ""

class User(_UserBase):
    def __init__(self, id, rest):
        super().__init__(id, rest)
