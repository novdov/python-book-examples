from collections import abc
from typing import Mapping


class FrozenJSON:
    def __init__(self, mapping: Mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name: str):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj: object):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        return obj
