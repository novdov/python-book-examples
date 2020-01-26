"""
20.1.2
"""

from typing import Any


class Quantity:
    __counter = 0

    def __init__(self) -> None:
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f"_{prefix}#{index}"
        cls.__counter += 1

    def __get__(self, instance: object, owner: object):
        return getattr(instance, self.storage_name)

    def __set__(self, instance: object, value: Any) -> None:
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError("value must be > 0")


class LineItem:
    """LineItem v4: Auto property name"""

    weight = Quantity()
    price = Quantity()

    def __init__(self, description: str, weight: float, price: float):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self) -> float:
        return self.weight * self.price


if __name__ == "__main__":
    coconuts = LineItem("Brazilian coconut", 20, 17.95)
    print(coconuts.weight, coconuts.price)
    print(getattr(coconuts, "_Quantity#0"), getattr(coconuts, "_Quantity#1"))
