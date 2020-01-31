from typing import Any
from weakref import WeakKeyDictionary


class DescriptorClass:
    def __init__(self, initial_value: Any):
        self.value = initial_value
        self.mapping = WeakKeyDictionary()

    def __get__(self, instance: object, owner: object):
        if instance is None:
            return self
        return self.mapping.get(instance, self.value)

    def __set__(self, instance: object, value: Any):
        self.mapping[instance] = value


class ClientClass:
    descriptor = DescriptorClass("default value")


if __name__ == "__main__":
    client1 = ClientClass()
    client2 = ClientClass()

    client1.descriptor = "new value"
    print(client1.descriptor)
    print(client2.descriptor)

    client2.descriptor = "value for client 2"
    print(client2.descriptor)
    print(client2.descriptor != client1.descriptor)
