from typing import Generator


def record_factory(cls_name, field_names: str) -> type:
    try:
        field_names = field_names.replace(",", " ").split()
    # When cannot use `replace` or `split`
    except AttributeError:
        pass

    field_names = tuple(field_names)

    def __init__(self: object, *args, **kwargs) -> None:
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self: object) -> Generator:
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self: object) -> str:
        values = ", ".join("{}={!r}".format(*i) for i in zip(self.__slots__, self))
        return f"{self.__class__.__name__}({values})"

    cls_attrs = dict(
        __slots__=field_names, __init__=__init__, __iter__=__iter__, __repr__=__repr__,
    )
    return type(cls_name, (object,), cls_attrs)


if __name__ == "__main__":
    Dog = record_factory("Dog", "name weight owner")
    rex = Dog("Rex", 30, "Bob")
    name, weight, _ = rex
    print(name, weight)
    print(Dog.__mro__)
