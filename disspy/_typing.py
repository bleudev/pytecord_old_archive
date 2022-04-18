from typing import Type


class TypeOf:
    def __new__(cls, *args, **kwargs):
        _type = list(args)[0]
        _obj = _type()
        _all = _obj.__all__()

        return Type[_all[0]]
