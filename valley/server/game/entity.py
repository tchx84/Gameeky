from typing import Dict, List

from ...common.action import Action
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.entity import Vector
from ...common.utils import get_time_milliseconds
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    def __init__(self, velocity: float, solid: bool, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.velocity = velocity
        self.solid = solid

        self._last_action = None
        self._last_timestamp = None

    def _get_elapsed_milliseconds(self):
        if self.action != self._last_action:
            self._last_timestamp = get_time_milliseconds()

        timestamp = get_time_milliseconds()
        elapsed = timestamp - self._last_timestamp

        self._last_action = self.action
        self._last_timestamp = timestamp

        return elapsed

    def idle(self):
        self._get_elapsed_milliseconds()

    def move(self, obstacles: List["Entity"]) -> None:
        elapsed_seconds = self._get_elapsed_milliseconds() / 1000

        for obstacle in obstacles:
            if obstacle.solid is True:
                return

        distance = self.velocity * elapsed_seconds

        if self.direction == Direction.RIGHT:
            self.position.x += distance
        elif self.direction == Direction.UP:
            self.position.y -= distance
        elif self.direction == Direction.LEFT:
            self.position.x -= distance
        elif self.direction == Direction.DOWN:
            self.position.y += distance


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
            solid=description.game.default.solid,
            direction=Direction[description.game.default.direction.upper()],
            action=Action[description.game.default.action.upper()],
        )
