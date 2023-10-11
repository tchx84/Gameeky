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


class Entity(Serializeable):
    Signature = Tuple[int, int, Vector.Signature, int, float, int]

    def __init__(
        self,
        id: int,
        type_id: int = 0,
        position: Optional[Vector] = None,
        direction: Direction = Direction.RIGHT,
        velocity: float = 0.05,
        action: Action = Action.NOTHING,
    ) -> None:
        self.id = id
        self.type_id = type_id
        self.position = position if position else Vector()
        self.direction = direction
        self.velocity = velocity
        self.action = action

    def to_values(self) -> Signature:
        return (
            self.id,
            self.type_id,
            self.position.to_values(),
            self.direction,
            self.velocity,
            self.action,
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Entity":
        id, type_id, position, direction, velocity, action = values
        return cls(
            id,
            type_id,
            Vector.from_values(position),
            Direction(direction),
            velocity,
            Action(action),
        )
