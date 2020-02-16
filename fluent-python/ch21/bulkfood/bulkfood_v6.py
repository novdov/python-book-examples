from . import model_v6 as model


@model.entity
class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description: str, weight: float, price: float):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self) -> float:
        return self.weight * self.price
