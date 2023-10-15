from enum import IntEnum

from typing import Optional, Tuple

from .state import State
from .direction import Direction
from .serializeable import Serializeable


class Vector(Serializeable):
    Signature = Tuple[float, float, float]

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def to_values(self) -> Signature:
        return (self.x, self.y, self.z)

    @classmethod
    def from_values(cls, values: Signature) -> "Vector":
        return cls(*values)


class EntityType(IntEnum):
    EMPTY = 0


class Entity(Serializeable):
    Signature = Tuple[int, int, Vector.Signature, int, int]

    def __init__(
        self,
        id: int,
        type_id: int,
        position: Optional[Vector] = None,
        direction: Direction = Direction.RIGHT,
        state: State = State.IDLING,
    ) -> None:
        self.id = id
        self.type_id = type_id
        self.position = position if position else Vector()
        self.direction = direction
        self.state = state

    def to_values(self) -> Signature:
        return (
            self.id,
            self.type_id,
            self.position.to_values(),
            self.direction,
            self.state,
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Entity":
        id, type_id, position, direction, state = values
        return cls(
            id,
            type_id,
            Vector.from_values(position),
            Direction(direction),
            State(state),
        )
