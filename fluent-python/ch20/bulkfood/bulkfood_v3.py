"""
20.1 디스크립터 예: 속성 검증
"""

from typing import Any


class Quantity:
    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def __set__(self, instance: object, value: Any) -> None:
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError("value must be > 0")


class LineItem:
    """LineItem v3: Simple descriptor"""

    weight = Quantity("weight")
    price = Quantity("price")

    def __init__(self, description: str, weight: float, price: float):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self) -> float:
        return self.weight * self.price
