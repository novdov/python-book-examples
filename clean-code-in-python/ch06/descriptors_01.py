import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DescriptorClass:
    def __get__(self, instance, owner):
        """
        Reference: https://docs.python.org/3/reference/datamodel.html#object.__get__

        Called to get the attribute of the owner class (class attribute access)
        or of an instance of that class (instance attribute access).
        The optional owner argument is the owner class,
        while instance is the instance that the attribute was accessed through,
        or None when the attribute is accessed through the owner.

        Args:
            instance: Object that calls descriptor. (client object)
            owner: Class of this object. (ClientClass)
        """
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
