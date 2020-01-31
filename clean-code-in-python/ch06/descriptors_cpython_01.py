from types import MethodType


class Method:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, instance, arg1, arg2):
        print(f"{self.name}: {instance} called with {arg1} and {arg2}")


class MyClass:
    method = Method("Internal call")


class NewMethod:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, instance, arg1, arg2):
        print(f"{self.name}: {instance} called with {arg1} and {arg2}")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return MethodType(self, instance)


class MyClass2:
    method = NewMethod("Internal call")


if __name__ == "__main__":
    # instance = MyClass()
    # Method("External call")(instance, "first", "second")
    # Below code does not work because `Method` is not a descriptor.
    # instance.method("first", "second")

    instance = MyClass2()
    NewMethod("External call")(instance, "first", "second")
    instance.method("first", "second")
