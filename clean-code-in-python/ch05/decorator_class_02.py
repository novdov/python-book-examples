from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


def hide_field(field: str) -> str:
    return "**redacted**"


def format_time(field_timestamp: datetime) -> str:
    return field_timestamp.strftime("%Y-%m-%d %H:%M")


def show_original(event_field: Any) -> Any:
    return event_field


class EventSerializer:
    def __init__(self, serialization_fields: Dict) -> None:
        self.serialization_fields = serialization_fields

    def serialize(self, event) -> Dict:
        return {
            field: transformation(getattr(event, field))
            for field, transformation in self.serialization_fields.items()
        }


class Serialization:
    def __init__(self, **transformations):
        self.serializer = EventSerializer(transformations)

    def __call__(self, event_class):
        def serialize_method(event_instance):
            return self.serializer.serialize(event_instance)

        event_class.serialize = serialize_method
        return event_class


@Serialization(
    username=str.lower, password=hide_field, ip=show_original, timestamp=format_time,
)
class LoginEvent:
    def __init__(self, username: str, password: str, ip: str, timestamp: datetime):
        self.username = username
        self.password = password
        self.ip = ip
        self.timestamp = timestamp


@Serialization(
    username=str.lower, password=hide_field, ip=show_original, timestamp=format_time,
)
@dataclass
class LoginEvent37:
    username: str
    password: str
    ip: str
    timestamp: datetime


if __name__ == "__main__":
    import pprint

    event = LoginEvent("UserName", "password", "127.0.0,1", datetime.now())
    pprint.pprint(event.serialize())
