import dispy.http.rest


class _UserBase:
    def __init__(self, id, rest: dispy.http.rest.Rest):
        self.id = id
        self._rest = rest

        # Data
        _data = self._rest.get("user", self.id)

        print(_data)
        try:
            _premium_type = int(_data["premium_type"])
        except KeyError:
            pass

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}#{self.discriminator}"

        try:
            self.isbot: bool = _data["bot"]
            self.issystem: bool = _data["system"]
            self.isverified: bool = _data["verified"]  # May be ""
        except KeyError:
            pass

        try:
            self.email: bool = _data["email"]  # May be ""
        except KeyError:
            pass

        self.flags: int = int(_data["public_flags"])
        try:
            self.nitro = DisNitro(_premium_type, _premium_type > 0)
        except UnboundLocalError:
            pass

    def uptade(self) -> None:
        _data = self._rest.get("user", self.id)
        _premium_type = int(_data["premium_type"])

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}{str(self.discriminator)}"

        self.isbot: bool = _data["bot"]
        self.issystem: bool = _data["system"]
        self.isverified: bool = _data["verified"]  # May be ""
        self.email: bool = _data["email"]  # May be ""
        self.flags: int = int(_data["public_flags"])

        self.nitro = DisNitro(_premium_type, _premium_type > 0)


class DisUser(_UserBase):
    def __init__(self, id, rest):
        super().__init__(id, rest)


class DisNitro:
    def __init__(self, type, ishave):
        self.classic = "classic"
        self.boost = "boost"
        self.none = "none"
        self.have = ishave

        if type == 1:
            self.type = self.classic
        elif type == 2:
            self.type = self.boost
        elif type == 0:
            self.type = self.none
        else:
            print("Invalid type of nitro!")
