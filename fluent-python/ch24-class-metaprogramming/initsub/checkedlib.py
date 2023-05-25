import inspect
from collections.abc import Callable
from typing import Any, NoReturn


class Field:
    def __init__(self, name: str, constructor: Callable):
        if not callable(constructor) or constructor is type(None):  # noqa: E721
            raise TypeError(f"{name!r} type hint must be a callable")

        self.name = name
        self.constructor = constructor

    def __set__(self, instance: Any, value: Any) -> None:
        if value is ...:
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)
            except (TypeError, ValueError) as exc:
                type_name = self.constructor.__name__
                msg = f"{value!r} is not compatible with {self.name}:{type_name}"
                raise TypeError(msg) from exc

        instance.__dict__[self.name] = value


class Checked:
    @classmethod
    def _fields(cls) -> dict[str, type]:
        return inspect.get_annotations(cls)

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        for name, constructor in cls._fields().items():
            setattr(cls, name, Field(name, constructor))

    def __init__(self, **kwargs: Any):
        for name in self._fields():
            value = kwargs.pop(name, ...)
            setattr(self, name, value)
        if kwargs:
            self.__flag_unknown_attrs(*kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._fields():
            cls = self.__class__
            descriptor = getattr(cls, name)
            descriptor.__set__(self, value)
        else:
            self.__flag_unknown_attrs(name)

    def __flag_unknown_attrs(self, *names: str) -> NoReturn:
        plural = "s" if len(names) > 1 else ""
        extra = ", ".join(repr(name) for name in names)
        cls_name = repr(self.__class__.__name__)
        raise AttributeError(f"{cls_name} object has no attribute{plural} {extra}")

    def _extra(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }
