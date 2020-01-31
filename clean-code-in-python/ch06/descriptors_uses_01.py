import functools
from datetime import datetime
from typing import Any, Callable, Dict


class BaseFieldTransformation:
    def __init__(self, transformation: Callable[[Any], str]):
        self._name = None
        self.transformation = transformation

    def __get__(self, instance: object, owner: object):
        if instance is None:
            return self
        raw_value = instance.__dict__[self._name]
        return self.transformation(raw_value)

    def __set_name__(self, owner: object, name: str):
        self._name = name

    def __set__(self, instance: object, value: Any):
        instance.__dict__[self._name] = value


ShowOriginal = functools.partial(BaseFieldTransformation, transformation=lambda x: x)
HideField = functools.partial(BaseFieldTransformation, transformation=lambda x: "**redacted**")
FormatTime = functools.partial(
    BaseFieldTransformation, transformation=lambda ft: ft.strftime("%Y-%m-%d %H:%M")
)


class LoginEvent:
    username = ShowOriginal()
    password = HideField()
    ip = ShowOriginal()
    timestamp = FormatTime()

    def __init__(self, username: str, password: str, ip: str, timestamp: datetime):
        self.username = username
        self.password = password
        self.ip = ip
        self.timestamp = timestamp

    def serialize(self) -> Dict:
        return {
            "username": self.username,
            "password": self.password,
            "ip": self.ip,
            "timestamp": self.timestamp,
        }


class BaseEvent:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def serialize(self) -> Dict:
        return {attr: getattr(self, attr) for attr in self._fields_to_serialize()}

    def _fields_to_serialize(self):
        for attr_name, value in vars(self.__class__).items():
            if isinstance(value, BaseFieldTransformation):
                yield attr_name


class NewLoginEvent(BaseEvent):
    username = ShowOriginal()
    password = HideField()
    ip = ShowOriginal()
    timestamp = FormatTime()


if __name__ == "__main__":
    le = LoginEvent("usr", "secret password", "127.0.0.1", datetime.utcnow())
    print(vars(le))
    print(le.serialize())
