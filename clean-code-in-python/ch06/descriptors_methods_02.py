from typing import Any, Callable


class Validation:
    def __init__(self, validation_function: Callable, error_msg: str):
        self.validation_function = validation_function
        self.error_msg = error_msg

    def __call__(self, value: Any):
        if not self.validation_function(value):
            raise ValueError(f"{value!r} {self.error_msg}")


class Field:
    def __init__(self, *validations: Validation):
        self._name = None
        self.validations = validations

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def validate(self, value: Any):
        for validation in self.validations:
            validation(value)

    def __set__(self, instance, value: Any):
        self.validate(value)
        instance.__dict__[self._name] = value


class ClientClass:
    descriptor = Field(
        Validation(lambda x: isinstance(x, (int, float)), "is not a number"),
        Validation(lambda x: x >= 0, "is less than 0"),
    )


if __name__ == "__main__":
    client = ClientClass()
    client.descriptor = 42
    print(client.descriptor)
    print(client.__dict__)
    # ValueError: -42 is less than 0
    client.descriptor = -42
    # ValueError: 'invalid value' is not a number
    client.descriptor = "invalid value"
