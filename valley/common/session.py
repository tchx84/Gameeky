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
    Signature = Tuple[()]

    def __init__(self) -> None:
        pass

    def to_values(self) -> Signature:
        return ()

    @classmethod
    def from_values(cls, values: Signature) -> "SessionRequest":
        return cls()
