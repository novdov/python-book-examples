from typing import Any


class SharedDataDescriptor:
    def __init__(self, initial_value: Any):
        self.value = initial_value

    def __get__(self, instance: object, owner: object):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance: object, value: Any):
        self.value = value


class ClientClass:
    descriptor = SharedDataDescriptor("first value")


if __name__ == "__main__":
    client1 = ClientClass()
    print(client1.descriptor)

    client2 = ClientClass()
    print(client2.descriptor)

    client2.descriptor = "value for client 2"
    print(client2.descriptor)
    print(client1.descriptor)
