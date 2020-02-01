from datetime import datetime
from typing import Dict


class LoginEventSerializer:
    def __init__(self, event):
        self.event = event

    def serialize(self) -> Dict:
        return {
            "username": self.event.username,
            "password": "**redacted**",
            "ip": self.event.ip,
            "timestamp": self.event.timestamp.strftime("%Y-%m-%d %H:%M"),
        }


class LoginEvent:
    SERIALIZER = LoginEventSerializer

    def __init__(self, username: str, password: str, ip: str, timestamp: datetime):
        self.username = username
        self.password = password
        self.ip = ip
        self.timestamp = timestamp

    def serialize(self) -> Dict:
        return self.SERIALIZER(self).serialize()


if __name__ == "__main__":
    import pprint

    event = LoginEvent("usr", "password", "127.0.0,1", datetime.now())
    pprint.pprint(event.serialize())
