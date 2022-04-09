import dispy.http.rest


class _UserBase:
    def __init__(self, id, rest: dispy.http.rest.Rest):
        self.id = id
        self._rest = rest

        # Data
        _data = self._rest.get("user", self.id)
        _premium_type = int(_data["premium_type"])

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}{self.discriminator}"

        self.isbot: bool = _data["bot"]
        self.issystem: bool = _data["system"]
        self.isverified: bool = _data["verified"]  # May be ""
        self.email: bool = _data["email"]  # May be ""
        self.flags: int = int(_data["flags"])

        self.nitro = Nitro(_premium_type, _premium_type > 0)

    def uptade(self) -> None:
        _data = self._rest.get("user", self.id)
        _premium_type = int(_data["premium_type"])

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}{self.discriminator}"

        self.isbot: bool = _data["bot"]
        self.issystem: bool = _data["system"]
        self.isverified: bool = _data["verified"]  # May be ""
        self.email: bool = _data["email"]  # May be ""
        self.flags: int = int(_data["public_flags"])

        self.nitro = Nitro(_premium_type, _premium_type > 0)


class User(_UserBase):
    def __init__(self, id, rest):
        super().__init__(id, rest)


class Nitro:
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
