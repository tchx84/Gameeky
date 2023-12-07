from typing import Tuple

from .serializeable import Serializeable


class Stats(Serializeable):
    Signature = Tuple[float, float, int]

    def __init__(
        self, durability: float = 0, stamina: float = 0, held: int = 0
    ) -> None:
        self.durability = durability
        self.stamina = stamina
        self.held = held

    def to_values(self) -> Signature:
        return (self.durability, self.stamina, self.held)

    @classmethod
    def from_values(cls, values: Signature) -> "Stats":
        return cls(*values)


class StatsRequest(Serializeable):
    Signature = Tuple[int]

    def __init__(self, session_id: int) -> None:
        self.session_id = session_id

    def to_values(self) -> Signature:
        return (self.session_id,)

    @classmethod
    def from_values(cls, values: Signature) -> "StatsRequest":
        return cls(*values)
