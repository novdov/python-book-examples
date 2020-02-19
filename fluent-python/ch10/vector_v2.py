import math
import numbers
import reprlib
from array import array
from typing import Iterable


class Vector:
    typecode = "d"

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self) -> Iterable:
        return iter(self._components)

    def __repr__(self) -> str:
        components = reprlib.repr(self._components)
        components = components[components.find("[") : -1]
        return f"Vector({components})"

    def __str__(self) -> str:
        return str(tuple(self))

    def __bytes__(self) -> bytes:
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __eq__(self, other) -> bool:
        return tuple(self) == tuple(other)

    def __abs__(self) -> float:
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __len__(self) -> int:
        return len(self._components)

    def __getitem__(self, index: int):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            raise TypeError(f"{cls.__name__} indices must be integers")

    @classmethod
    def frombytes(cls, octets) -> "Vector":
        typecode = chr(octets[0])
        memv = memoryview(octets[1:].cast(typecode))
        return cls(memv)
