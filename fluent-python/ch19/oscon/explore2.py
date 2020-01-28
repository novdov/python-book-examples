from collections import abc
from keyword import iskeyword
from typing import Mapping


class FrozenJSON:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping: Mapping):
        self.__data = dict()
        for key, value in mapping.items():
            if iskeyword(key):
                key += "_"
            self.__data[key] = value

    def __getattr__(self, name: str):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        return FrozenJSON(self.__data[name])
