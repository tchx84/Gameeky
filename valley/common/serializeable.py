import json

from typing import Any


class Serializeable(object):
    def serialize(self) -> bytes:
        return json.dumps(
            self, default=lambda o: Serializeable.filter(o.__dict__)
        ).encode("UTF-8")

    @staticmethod
    def filter(properties: dict) -> dict:
        return {
            name: properties[name] for name in properties if not name.startswith("_")
        }

    @classmethod
    def deserialize(cls, data: bytes) -> Any:
        return cls(**json.loads(data.decode("UTF-8")))
