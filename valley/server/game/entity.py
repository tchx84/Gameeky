import math

from typing import Dict, List, Optional, cast

from .partition import SpatialPartition

from ...common.action import Action
from ...common.state import State
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.entity import Vector
from ...common.utils import get_time_milliseconds
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    def __init__(
        self,
        velocity: float,
        durability: float,
        damage: float,
        duration: float,
        cooldown: float,
        removable: float,
        solid: bool,
        partition: SpatialPartition,
        *args,
        **kargs,
    ) -> None:
        super().__init__(*args, **kargs)
        self.velocity = velocity
        self.durability = durability
        self.damage = damage
        self.duration = duration
        self.cooldown = cooldown
        self.removable = removable
        self.solid = solid

        self._partition = partition
        self._busy = False
        self._action = Action.IDLE
        self._next_action = Action.IDLE
        self._next_value = 0.0
        self._target = Vector()
        self._held: Optional["Entity"] = None
        self._removed = False

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
        self._action = self._next_action
        self._busy = True

    def _prepare_move(self) -> None:
        self._action = self._next_action
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
        seconds_since_action = self._get_elapsed_seconds_since_action()

        # XXX Cooldown should depend on tool
        if seconds_since_action < self.cooldown:
            return

        self._action = self._next_action
        self._busy = True

    def _prepare_destroy(self):
        self._action = self._next_action
        self._busy = True

    def _prepare_take(self) -> None:
        if self._held is not None:
            return

        entities = cast(List["Entity"], self._partition.find_by_direction(self))
        if not entities:
            return

        entity = entities[-1]
        if entity.solid is False:
            return

        self._held = entity
        self._held.solid = False
        self._held.state = State.HELD

        self._action = self._next_action
        self._busy = True

    def _prepare_drop(self) -> None:
        if self._held is None:
            return

        self._held.state = State.IDLING
        self._held.solid = True
        self._held = None

        self._action = self._next_action
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
        elif self._next_action == Action.DESTROY:
            self._prepare_destroy()
        elif self._next_action == Action.TAKE:
            self._prepare_take()
        elif self._next_action == Action.DROP:
            self._prepare_drop()

        self._timestmap_prepare = get_time_milliseconds()

    def _check_status(self):
        if self.durability <= 0:
            self.perform(Action.DESTROY, 0)

    def _check_in_final_state(self):
        return self.state in [
            State.DESTROYED,
            State.HELD,
        ]

    def _update_held(self):
        if self._held is None:
            return

        self._partition.remove(self._held)

        self._held.position.x = self.position.x
        self._held.position.y = self.position.y
        self._held.direction = self.direction

        if self.direction == Direction.RIGHT:
            self._held.position.x += 1
        if self.direction == Direction.DOWN:
            self._held.position.y += 1
        if self.direction == Direction.LEFT:
            self._held.position.x -= 1
        if self.direction == Direction.UP:
            self._held.position.y -= 1

        self._partition.add(self._held)

    def tick(self) -> None:
        if self._check_in_final_state():
            return

        if self._action == Action.IDLE:
            self.idle()
        elif self._action == Action.MOVE:
            self.move()
        elif self._action == Action.USE:
            self.use()
        elif self._action == Action.DESTROY:
            self.destroy()
        elif self._action == Action.TAKE:
            self.take()
        elif self._action == Action.DROP:
            self.drop()

        self._update_held()
        self._check_status()
        self._prepare_next_tick()

        self._timestamp_tick = get_time_milliseconds()

    def idle(self) -> None:
        self.state = State.IDLING
        self._busy = False

    def move(self) -> None:
        self.state = State.MOVING

        seconds_since_tick = self._get_elapsed_seconds_since_tick()
        distance = self.velocity * seconds_since_tick

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
        self.state = State.USING

        seconds_since_tick = self._get_elapsed_seconds_since_tick()
        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        targets = cast(List["Entity"], self._partition.find_by_direction(self))
        damage = math.ceil(self.damage * seconds_since_tick)

        for target in targets:
            if target is not self._held:
                target.durability -= damage

        # XXX Usage time should depend on tool
        if seconds_since_prepare < self.duration:
            return

        self._action = Action.IDLE

        self._busy = False
        self._timestamp_action = get_time_milliseconds()

    def destroy(self):
        self.state = State.DESTROYING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare < self.duration:
            return

        self.state = State.DESTROYED
        self.solid = False
        self.position.z -= 1

        if self.removable:
            self._removed = True

        self._busy = False

    def take(self):
        self.state = State.TAKING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        # XXX duration can be a scaled by entity's weight'
        if seconds_since_prepare < self.duration / 2:
            return

        self.state = State.IDLING

        self._busy = False

    def drop(self):
        self.state = State.DROPPING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        # XXX duration can be a scaled by entity's weight'
        if seconds_since_prepare < self.duration / 4:
            return

        self.state = State.IDLING

        self._busy = False

    def perform(self, action: Action, value: float) -> None:
        self._next_action = action
        self._next_value = value

    def removed(self):
        return self._removed


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
            durability=description.game.default.durability,
            damage=description.game.default.damage,
            cooldown=description.game.default.cooldown,
            duration=description.game.default.duration,
            removable=description.game.default.removable,
            solid=description.game.default.solid,
            direction=Direction[description.game.default.direction.upper()],
            state=State[description.game.default.state.upper()],
            partition=partition,
        )
