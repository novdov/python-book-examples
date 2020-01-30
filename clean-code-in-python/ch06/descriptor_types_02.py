import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger(__name__)


class DataDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return 42

    def __set__(self, instance, value):
        logger.debug(f"setting {instance}.descriptor to {value}")
        # Cause infinite loop: setattr -> __set__ -> setattr -> ...
        # setattr(instance, "descriptor", value)
        instance.__dict__["descriptor"] = value


class ClientClass:
    descriptor = DataDescriptor()


if __name__ == "__main__":
    # When __set__ method is implemented,
    # python find attribute descriptor class first, rather than __dict__ of that object.
    # Deletion also does not work anymore. (`__delete__` method should be implemented.)
    client = ClientClass()
    print(client.descriptor)

    client.descriptor = 99
    # Value of descriptor does not change.
    print(client.descriptor)
    # {'descriptor': 99}
    print(vars(client))
    # 99
    print(client.__dict__["descriptor"])
