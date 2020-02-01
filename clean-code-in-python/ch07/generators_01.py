from typing import Generator, List

from _generate_data import PURCHASES_FILE, create_purchases_file

from utils.logger import logger


class PurchaseStats:
    def __init__(self, purchases):
        self.purchases = iter(purchases)
        self.min_price = None
        self.max_price = None
        self._total_purchases_price = 0.0
        self._total_purchases = 0
        self._initialize()

    def _initialize(self) -> None:
        try:
            first_value = next(self.purchases)
        except StopIteration:
            raise ValueError("no values provided")

        self.min_price = self.max_price = first_value
        self._update_avg(first_value)

    def process(self) -> "PurchaseStats":
        for purchase_value in self.purchases:
            self._update_min(purchase_value)
            self._update_max(purchase_value)
            self._update_avg(purchase_value)
        return self

    def _update_min(self, new_value: float) -> None:
        if new_value < self.min_price:
            self.min_price = new_value

    def _update_max(self, new_value: float) -> None:
        if new_value > self.max_price:
            self.max_price = new_value

    def _update_avg(self, new_value: float) -> None:
        self._total_purchases_price += new_value
        self._total_purchases += 1

    @property
    def avg_price(self) -> float:
        return self._total_purchases_price / self._total_purchases

    def __str__(self):
        return f"{self.__class__.__name__}({self.min_price}, {self.max_price}, {self.avg_price})"


def _load_purchases(filename: str) -> List:
    purchases = []
    with open(filename) as f:
        for line in f:
            *_, price_raw = line.partition(",")
            purchases.append(float(price_raw))
    return purchases


def load_purchases(filename: str) -> Generator:
    with open(filename) as f:
        for line in f:
            *_, price_raw = line.partition(",")
            yield float(price_raw)


def main():
    create_purchases_file(PURCHASES_FILE)
    purchases = load_purchases(PURCHASES_FILE)
    stats = PurchaseStats(purchases).process()
    logger.info(f"Results: {stats}")


if __name__ == "__main__":
    main()
