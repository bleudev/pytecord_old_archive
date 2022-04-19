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

from disspy import errs


class _UserBase:
    def __init__(self, id, api, premium_gets):
        self.id = id
        self._api = api

        # Data
        _data = self._api.get_user_json(id)
        if premium_gets:
            try:
                _premium_type = int(_data["premium_type"])
            except KeyError:
                _premium_type = -1
                raise errs.MissingPerms(errs.missingperms)

            self.username = _data["username"]
            self.discriminator = _data["discriminator"]
            self.fullname = f"{self.username}#{self.discriminator}"

            try:
                self.isbot: bool = _data["bot"]
            except KeyError:
                del self.isbot
                raise errs.MissingPerms(errs.missingperms)

            try:
                self.issystem: bool = _data["system"]
            except KeyError:
                del self.issystem
                raise errs.MissingPerms(errs.missingperms)

            try:
                self.isverified: bool = _data["verified"]  # May be ""
            except KeyError:
                del self.isverified
                raise errs.MissingPerms(errs.missingperms)

            try:
                self.email: bool = _data["email"]  # May be ""
            except KeyError:
                del self.email
                raise errs.MissingPerms(errs.missingperms)

            self.flags: int = int(_data["public_flags"])

            self.nitro = DisNitro(_premium_type, _premium_type != 0 and _premium_type != -1)
        else:
            _premium_type = -1
            try:
                self.flags: int = int(_data["public_flags"])
            except KeyError:
                pass
            try:
                self.username = _data["username"]
                self.discriminator = _data["discriminator"]
                self.fullname = f"{self.username}#{self.discriminator}"
            except KeyError:
                pass

    def update(self) -> None:
        _data = self._api.get_user_json(self.id)

        try:
            _premium_type = int(_data["premium_type"])
        except KeyError:
            _premium_type = -1

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}{str(self.discriminator)}"
        try:
            self.isbot: bool = _data["bot"]
            self.issystem: bool = _data["system"]
            self.isverified: bool = _data["verified"]  # May be ""
            self.email: bool = _data["email"]  # May be ""
        except KeyError:
            pass

        self.flags: int = int(_data["public_flags"])

        try:
            self.nitro = DisNitro(_premium_type, _premium_type != 0 and _premium_type != -1)
        except UnboundLocalError:
            pass


class DisUser(_UserBase):
    def __init__(self, id, rest, premium_gets):
        super().__init__(id, rest, premium_gets)


class DisNitro:
    def __init__(self, type, ishave):
        self.classic = "classic"
        self.boost = "boost"
        self.none = "none"
        if type != -1:
            self.have = ishave
        else:
            del self.have
        if type == 1:
            self.type = self.classic
        elif type == 2:
            self.type = self.boost
        elif type == -1:
            raise errs.MissingPerms(errs.missingperms)
        elif type == 0:
            self.type = self.none
        else:
            raise errs.UserNitroTypeError("Invalid type of error!")
