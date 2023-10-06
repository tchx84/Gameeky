from typing import Tuple

from .serializeable import Serializeable


class Session(Serializeable):
    SIGNATURE = "(ii)"

    def __init__(self, id: int, entity_id: int) -> None:
        self.id = id
        self.entity_id = entity_id

    def to_values(self):
        return (self.id, self.entity_id)

    @classmethod
    def from_values(cls, values: Tuple[int, int]) -> "Session":
        return cls(*values)


class SessionRequest(Serializeable):
    def __init__(self) -> None:
        pass

    def to_values(self):
        return ()

    @classmethod
    def from_values(cls, values: Tuple) -> "SessionRequest":
        return cls()
