import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DescriptorClass:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        logger.info(f"Call: {self.__class__.__name__}.__get__({repr(instance)}, {repr(owner)})")
        return instance


class ClientClass:
    descriptor = DescriptorClass()


if __name__ == "__main__":
    client = ClientClass()
    print(client.descriptor)
    print(client.descriptor is client)
