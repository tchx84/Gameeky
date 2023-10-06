import json

from typing import Any


class Serializeable(object):
    SIGNATURE = ""

    def to_values(self) -> Any:
        raise NotImplementedError

    @classmethod
    def from_values(cls, values: Any) -> Any:
        raise NotImplementedError

    def serialize(self):
        return json.dumps(self.to_values()).encode("UTF-8")

    @classmethod
    def deserialize(cls, data: bytes) -> Any:
        values = json.loads(data.decode("UTF-8"))
        return cls.from_values(values)
