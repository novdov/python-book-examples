from typing import List


class Traveller:
    def __init__(self, name: str, current_city: str):
        self.name = name
        self._current_city = current_city
        self._cities_visited = [current_city]

    @property
    def current_city(self) -> str:
        return self._current_city

    @current_city.setter
    def current_city(self, new_city: str) -> None:
        if new_city != self._current_city:
            self._cities_visited.append(new_city)
        self._current_city = new_city

    @property
    def cities_visited(self) -> List[str]:
        return self._cities_visited


if __name__ == "__main__":
    alice = Traveller("Alice", "Barcelona")
    alice.current_city = "Paris"
    alice.current_city = "Brussels"
    alice.current_city = "Amsterdam"
    print(alice.cities_visited)
