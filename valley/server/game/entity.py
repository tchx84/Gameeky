import math

from typing import Dict, List, Optional, cast

from .definitions import Density
from .partition import SpatialPartition

from ...common.action import Action
from ...common.state import State
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.entity import Vector
from ...common.utils import get_time_milliseconds
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    __stamina_percent_by_action__ = {
        Action.IDLE: 0.1,
        Action.MOVE: -0.05,
        Action.USE: -0.2,
        Action.TAKE: -0.2,
        Action.DROP: 0,
        Action.DESTROY: 0,
        Action.EXHAUST: 0.1,
    }

    def __init__(
        self,
        stamina: float,
        durability: float,
        weight: float,
        strength: float,
        duration: float,
        removable: float,
        density: Density,
        partition: SpatialPartition,
        *args,
        **kargs,
    ) -> None:
        super().__init__(*args, **kargs)
        self.stamina = stamina
        self.durability = durability
        self.weight = weight
        self.strength = strength
        self.duration = duration
        self.removable = removable
        self.density = density

        self._partition = partition
        self._busy = False
        self._action = Action.IDLE
        self._next_action = Action.IDLE
        self._next_value = 0.0
        self._target = Vector()
        self._held: Optional["Entity"] = None
        self._max_stamina = self.stamina
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
            if obstacle.density == Density.SOLID:
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

        # Don't go outside'of the scene
        self._target.x = min(max(self._target.x, 0), self._partition.width - 1)
        self._target.y = min(max(self._target.y, 0), self._partition.height - 1)

        self._busy = True

    def _prepare_use(self) -> None:
        seconds_since_action = self._get_elapsed_seconds_since_action()

        # XXX Cooldown should depend on tool
        if seconds_since_action < self.duration:
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
        if entity.density == Density.VOID:
            return

        self._held = entity
        self._held.density = Density.VOID
        self._held.state = State.HELD

        self._action = self._next_action
        self._busy = True

    def _prepare_drop(self) -> None:
        if self._held is None:
            return

        self._action = self._next_action
        self._busy = True

    def _prepare_exhaust(self):
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
        elif self._next_action == Action.EXHAUST:
            self._prepare_exhaust()

        self._timestmap_prepare = get_time_milliseconds()

    def _do_idle(self) -> None:
        self.state = State.IDLING
        self._busy = False

    def _do_move(self) -> None:
        self.state = State.MOVING

        surfaces = cast(List["Entity"], self._partition.find_by_position(self.position))
        friction = 1.0 - surfaces[0].density

        seconds_since_tick = self._get_elapsed_seconds_since_tick()
        weight = self.weight + self._held.weight if self._held else self.weight
        distance = (self.strength / weight) * friction * seconds_since_tick

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

        self._action = Action.IDLE
        self._busy = False

    def _do_use(self) -> None:
        self.state = State.USING

        seconds_since_tick = self._get_elapsed_seconds_since_tick()
        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        targets = cast(List["Entity"], self._partition.find_by_direction(self))
        wear = math.ceil(self.strength * seconds_since_tick)

        for target in targets:
            if target is not self._held:
                target.durability -= wear

        # XXX Usage time should depend on tool
        if seconds_since_prepare < self.duration:
            return

        self._action = Action.IDLE
        self._busy = False
        self._timestamp_action = get_time_milliseconds()

    def _do_destroy(self):
        self.state = State.DESTROYING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare < self.duration:
            return

        self.state = State.DESTROYED
        self.density = Density.VOID
        self.position.z -= 1

        self._drop()

        if self.removable:
            self._removed = True

        self._busy = False

    def _do_take(self):
        self.state = State.TAKING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()
        ratio = self._held.weight / self.strength

        if seconds_since_prepare < self.duration * ratio:
            return

        self._action = Action.IDLE
        self._busy = False

    def _do_drop(self):
        self.state = State.DROPPING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare < self.duration:
            return

        self._drop()

        self._action = Action.IDLE
        self._busy = False

    def _do_exhaust(self):
        self.state = State.EXHAUSTED

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare < self.duration * 5.0:
            return

        self._drop()

        # Interrupt the action provided by the client
        self.perform(Action.IDLE, 0)
        self._busy = False

    def _drop(self):
        if self._held is None:
            return

        self._held.density = Density.SOLID
        self._held.state = State.IDLING
        self._held = None

    def _check_attributes(self):
        if self.durability <= 0:
            self.perform(Action.DESTROY, 0)
        if self.stamina <= 0:
            self.perform(Action.EXHAUST, self.direction)

    def _check_in_blocking_state(self):
        return self.state in [
            State.DESTROYED,
            State.HELD,
        ]

    def _update_stamina(self) -> None:
        seconds_since_tick = self._get_elapsed_seconds_since_tick()

        percent = self.__stamina_percent_by_action__.get(self._action, 0)
        modifier = (self._max_stamina * percent) * seconds_since_tick

        self.stamina = max(min(self.stamina + modifier, self._max_stamina), 0)

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
        if self._check_in_blocking_state():
            return

        if self._action == Action.IDLE:
            self._do_idle()
        elif self._action == Action.MOVE:
            self._do_move()
        elif self._action == Action.USE:
            self._do_use()
        elif self._action == Action.DESTROY:
            self._do_destroy()
        elif self._action == Action.TAKE:
            self._do_take()
        elif self._action == Action.DROP:
            self._do_drop()
        elif self._action == Action.EXHAUST:
            self._do_exhaust()

        self._check_attributes()
        self._update_stamina()
        self._update_held()
        self._prepare_next_tick()

        self._timestamp_tick = get_time_milliseconds()

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
            stamina=description.game.default.stamina,
            durability=description.game.default.durability,
            weight=description.game.default.weight,
            strength=description.game.default.strength,
            duration=description.game.default.duration,
            removable=description.game.default.removable,
            density=description.game.default.density,
            direction=Direction[description.game.default.direction.upper()],
            state=State[description.game.default.state.upper()],
            partition=partition,
        )
