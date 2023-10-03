from typing import Optional

from .action import Action
from .serializeable import Serializeable


class Vector(Serializeable):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y


class Entity(Serializeable):
    def __init__(
        self,
        id: int,
        position: Optional[Vector] = None,
        angle: float = 0,
        velocity: float = 1.0,
        action: Action = Action.NOTHING,
    ) -> None:
        self.id = id
        self.position = position if position else Vector()
        self.angle = angle
        self.velocity = velocity
        self.action = action
