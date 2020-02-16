import abc


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f"_{prefix}#{index}"
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """Return validated value or raise ValueError"""


class Quantity(Validated):
    """A number greater than 0"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError("value must be > 0")
        return value


class NonBlank(Validated):
    """A string with at least one non-space character"""

    def validate(self, instance, value: str):
        value = value.strip()
        if not value:
            raise ValueError("value cannot be empty or blank")
        return value


class EntityMeta(type):
    """Metaclass for business entities with validated fields."""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = f"_{type_name}#{key}"


class Entity(metaclass=EntityMeta):
    """Business entity with validated fields."""
