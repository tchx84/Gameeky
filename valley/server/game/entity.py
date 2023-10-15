import math

from typing import Dict, List, cast

from .partition import SpatialPartition

from ...common.action import Action
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.entity import Vector
from ...common.utils import get_time_milliseconds
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    def __init__(
        self,
        velocity: float,
        solid: bool,
        partition: SpatialPartition,
        *args,
        **kargs,
    ) -> None:
        super().__init__(*args, **kargs)
        self.velocity = velocity
        self.solid = solid

        self._partition = partition
        self._busy = False
        self._next_action = Action.IDLE
        self._next_value = 0.0
        self._target = Vector()

        timestamp = get_time_milliseconds()
        self._timestmap_prepare = timestamp
        self._timestamp_tick = timestamp
        self._timestamp_action = timestamp

    def _get_elapsed_seconds_since_tick(self) -> float:
        return (get_time_milliseconds() - self._timestamp_tick) / 1000

    def _get_elapsed_seconds_since_prepare(self) -> float:
        return (get_time_milliseconds() - self._timestmap_prepare) / 1000

    def _get_elapsed_seconds_since_action(self) -> float:
        return (get_time_milliseconds() - self._timestamp_action) / 1000

    def _prepare_idle(self) -> None:
        self.action = self._next_action
        self._busy = True

    def _prepare_move(self) -> None:
        self.action = self._next_action
        self.direction = Direction(int(self._next_value))

        obstacles = cast(List["Entity"], self._partition.find_by_direction(self))

        # Don't allow walking in empty space
        if not obstacles:
            return

        for obstacle in obstacles:
            if obstacle.solid:
                return

        self._target = Vector(
            x=math.floor(self.position.x),
            y=math.floor(self.position.y),
        )

        if self.direction == Direction.RIGHT:
            self._target.x += 1
        elif self.direction == Direction.UP:
            self._target.y -= 1
        elif self.direction == Direction.LEFT:
            self._target.x -= 1
        elif self.direction == Direction.DOWN:
            self._target.y += 1

        self._busy = True

    def _prepare_use(self) -> None:
        elapsed_seconds = self._get_elapsed_seconds_since_action()

        # XXX Cooldown should depend on tool
        if elapsed_seconds < 1.0:
            return

        self.action = self._next_action
        self._busy = True

    def _prepare_next_tick(self) -> None:
        if self._busy is True:
            return

        if self._next_action == Action.IDLE:
            self._prepare_idle()
        elif self._next_action == Action.MOVE:
            self._prepare_move()
        elif self._next_action == Action.USE:
            self._prepare_use()

        self._timestmap_prepare = get_time_milliseconds()

    def tick(self) -> None:
        if self.action == Action.IDLE:
            self.idle()
        elif self.action == Action.MOVE:
            self.move()
        elif self.action == Action.USE:
            self.use()

        self._prepare_next_tick()

        self._timestamp_tick = get_time_milliseconds()

    def idle(self) -> None:
        self._busy = False

    def move(self) -> None:
        elapsed_seconds = self._get_elapsed_seconds_since_tick()
        distance = self.velocity * elapsed_seconds

        delta_x = self._target.x - self.position.x
        delta_y = self._target.y - self.position.y

        distance_x = min(distance, abs(delta_x))
        distance_y = min(distance, abs(delta_y))

        direction_x = math.copysign(1, delta_x)
        direction_y = math.copysign(1, delta_y)

        self._partition.remove(self)

        self.position.x += distance_x * direction_x
        self.position.y += distance_y * direction_y

        self._partition.add(self)

        if self.position.x != self._target.x:
            return
        if self.position.y != self._target.y:
            return

        self._busy = False

    def use(self) -> None:
        elapsed_seconds = self._get_elapsed_seconds_since_prepare()
        targets = self._partition.find_by_direction(self)

        # XXX It has no effect yet
        for target in targets:
            pass

        # XXX Usage time should depend on tool
        if elapsed_seconds < 1.0:
            return

        self.action = Action.IDLE

        self._busy = False
        self._timestamp_action = get_time_milliseconds()

    def perform(self, action: Action, value: float) -> None:
        self._next_action = action
        self._next_value = value


class EntityRegistry:
    __entities__: Dict[int, Description] = {}

    @classmethod
    def register(cls, description: Description) -> None:
        cls.__entities__[description.id] = description

    @classmethod
    def new_from_values(
        cls,
        id: int,
        type_id: int,
        position: Vector,
        partition: SpatialPartition,
    ) -> Entity:
        description = cls.__entities__[type_id]
        return Entity(
            id=id,
            type_id=type_id,
            position=position,
            velocity=description.game.default.velocity,
            solid=description.game.default.solid,
            direction=Direction[description.game.default.direction.upper()],
            action=Action[description.game.default.action.upper()],
            partition=partition,
        )
