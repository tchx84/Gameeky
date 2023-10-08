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
    Signature = Tuple[int, Vector.Signature, float, float, int]

    def __init__(
        self,
        id: int,
        position: Optional[Vector] = None,
        angle: float = Direction.RIGHT,
        velocity: float = 0.05,
        action: Action = Action.NOTHING,
    ) -> None:
        self.id = id
        self.position = position if position else Vector()
        self.angle = angle
        self.velocity = velocity
        self.action = action

    def to_values(self) -> Signature:
        return (
            self.id,
            self.position.to_values(),
            self.angle,
            self.velocity,
            self.action,
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Entity":
        id, position, angle, velocity, action = values
        return cls(id, Vector.from_values(position), angle, velocity, Action(action))
