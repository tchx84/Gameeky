from typing import Tuple

from .serializeable import Serializeable


class Session(Serializeable):
    Signature = Tuple[int]

    def __init__(self, id: int) -> None:
        self.id = id

    def to_values(self) -> Signature:
        return (self.id,)

    @classmethod
    def from_values(cls, values: Signature) -> "Session":
        return cls(*values)


class SessionRequest(Serializeable):
    Signature = Tuple[int]

    def __init__(self, type_id: int) -> None:
        self.type_id = type_id

    def to_values(self) -> Signature:
        return (self.type_id,)

    @classmethod
    def from_values(cls, values: Signature) -> "SessionRequest":
        return cls(*values)
