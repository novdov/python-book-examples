# Descriptors methods 01: __get__


class DescriptorClass:
    def __get__(self, instance, owner):
        if instance is None:
            return f"{self.__class__.__name__}.{owner.__name__}"
        return f"value for {instance}"


class ClientClass:
    descriptor = DescriptorClass()


if __name__ == "__main__":
    # "DescriptorClass.ClientClass"
    print(ClientClass.descriptor)

    # "value for <__main__.ClientClass object at 0x...>
    print(ClientClass().descriptor)
