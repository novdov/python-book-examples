class NonDataDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return 42


class ClientClass:
    descriptor = NonDataDescriptor()


if __name__ == "__main__":
    client = ClientClass()
    # Cannot find "descriptor" in client.__dict__
    # Find descriptor in client (descriptor.__get__)
    print(client.descriptor)

    client.descriptor = 43
    print(client.descriptor)

    del client.descriptor
    print(client.descriptor)
