from typing import Tuple

from .serializeable import Serializeable


class Session(Serializeable):
    Signature = Tuple[int, int]

    def __init__(self, id: int, entity_id: int) -> None:
        self.id = id
        self.entity_id = entity_id

    def to_values(self) -> Signature:
        return (self.id, self.entity_id)

    @classmethod
    def from_values(cls, values: Signature) -> "Session":
        return cls(*values)


class SessionRequest(Serializeable):
    Signature = Tuple[()]

    def __init__(self) -> None:
        pass

    def to_values(self) -> Signature:
        return ()

    @classmethod
    def from_values(cls, values: Signature) -> "SessionRequest":
        return cls()
