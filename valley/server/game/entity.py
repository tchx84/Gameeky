from typing import Dict

from ...common.action import Action
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.entity import Vector
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    def __init__(self, velocity: float, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.velocity = velocity

    def move(self) -> None:
        if self.direction == Direction.RIGHT:
            self.position.x += self.velocity
        elif self.direction == Direction.UP:
            self.position.y -= self.velocity
        elif self.direction == Direction.LEFT:
            self.position.x -= self.velocity
        elif self.direction == Direction.DOWN:
            self.position.y += self.velocity


class EntityRegistry:
    __entities__: Dict[int, Description] = {}

    @classmethod
    def register(cls, description: Description) -> None:
        cls.__entities__[description.id] = description

    @classmethod
    def new_from_values(cls, id: int, type_id: int, position: Vector) -> Entity:
        description = cls.__entities__[type_id]
        return Entity(
            id=id,
            type_id=type_id,
            position=position,
            velocity=description.game.default.velocity,
            direction=Direction[description.game.default.direction.upper()],
            action=Action[description.game.default.action.upper()],
        )
