from typing import Optional, Tuple

from .action import Action
from .direction import Direction
from .serializeable import Serializeable


class Vector(Serializeable):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def to_values(self):
        return (self.x, self.y)

    @classmethod
    def from_values(cls, values: Tuple[float, ...]) -> "Vector":
        return cls(*values)


class Entity(Serializeable):
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

    def to_values(self):
        return (
            self.id,
            self.position.to_values(),
            self.angle,
            self.velocity,
            self.action,
        )

    @classmethod
    def from_values(
        cls,
        values: Tuple[int, Tuple[float, ...], float, float, int],
    ) -> "Entity":
        id, position, angle, velocity, action = values
        return cls(id, Vector.from_values(position), angle, velocity, Action(action))
