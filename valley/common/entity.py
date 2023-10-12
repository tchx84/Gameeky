from enum import IntEnum

from typing import Optional, Tuple

from .action import Action
from .direction import Direction
from .serializeable import Serializeable


class Vector(Serializeable):
    Signature = Tuple[float, float]

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def to_values(self) -> Signature:
        return (self.x, self.y)

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
        action: Action = Action.IDLE,
    ) -> None:
        self.id = id
        self.type_id = type_id
        self.position = position if position else Vector()
        self.direction = direction
        self.action = action

    def to_values(self) -> Signature:
        return (
            self.id,
            self.type_id,
            self.position.to_values(),
            self.direction,
            self.action,
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Entity":
        id, type_id, position, direction, action = values
        return cls(
            id,
            type_id,
            Vector.from_values(position),
            Direction(direction),
            Action(action),
        )
