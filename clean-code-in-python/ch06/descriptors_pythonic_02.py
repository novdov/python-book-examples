from typing import Any


class HistoryTracedAttribute:
    def __init__(self, trace_attribute_name: str):
        self.trace_attribute_name = trace_attribute_name
        self._name = None

    def __set_name__(self, owner: object, name: str) -> None:
        self._name = name

    def __get__(self, instance: object, owner: object) -> Any:
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance: object, value: Any) -> None:
        self._track_change_in_value_for_instance(instance, value)
        instance.__dict__[self._name] = value

    def _track_change_in_value_for_instance(self, instance: object, value: Any) -> None:
        self._set_default(instance)
        if self._needs_to_track_change(instance, value):
            instance.__dict__[self.trace_attribute_name].append(value)

    def _needs_to_track_change(self, instance: object, value: Any) -> bool:
        try:
            current_value = instance.__dict__[self._name]
        except KeyError:
            return True
        return value != current_value

    def _set_default(self, instance: object) -> None:
        instance.__dict__.setdefault(self.trace_attribute_name, [])


class Traveller:
    current_city = HistoryTracedAttribute("cities_visited")

    def __init__(self, name: str, current_city: str):
        self.name = name
        self.current_city = current_city
