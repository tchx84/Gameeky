import math

from copy import deepcopy
from typing import Dict, List, Optional, cast

from .definitions import Density, Recovery, Penalty, Delay, Cost
from .partition import SpatialPartition

from .actuators.base import Actuator
from .actuators.grower import Actuator as GrowerActuator
from .actuators.portal import Actuator as PortalActuator
from .actuators.portal_area import Actuator as PortalAreaActuator

from ...common.action import Action
from ...common.state import State
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.entity import Vector
from ...common.utils import get_time_milliseconds, clamp
from ...common.entity import EntityType
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    __entity_by_name__: Dict[str, "Entity"] = {}

    __stamina_cost_by_action__ = {
        Action.MOVE: Cost.MAX,
        Action.USE: Cost.MAX * 4,
        Action.TAKE: Cost.MAX * 4,
    }

    __actuator_by_name__ = {
        GrowerActuator.name: GrowerActuator,
        PortalActuator.name: PortalActuator,
        PortalAreaActuator.name: PortalAreaActuator,
    }

    def __init__(
        self,
        stamina: float,
        durability: float,
        weight: float,
        strength: float,
        recovery: float,
        removable: float,
        equippable: bool,
        density: Density,
        spawns: int,
        name: str,
        actuator: str,
        target: str,
        radius: float,
        rate: float,
        partition: SpatialPartition,
        *args,
        **kargs,
    ) -> None:
        super().__init__(*args, **kargs)
        self.stamina = stamina
        self.durability = durability
        self.weight = weight
        self.strength = strength
        self.recovery = clamp(Recovery.MAX, Recovery.MIN, recovery)
        self.removable = removable
        self.equippable = equippable
        self.density = clamp(Density.SOLID, Density.VOID, density)
        self.spawns = spawns
        self.name = name
        self.actuator: Optional[Actuator] = None
        self.target = target
        self.radius = radius
        self.rate = rate

        if ActuatorClass := self.__actuator_by_name__.get(actuator):
            self.actuator = ActuatorClass(self)

        self._partition = partition
        self._busy = False
        self._spawned = EntityType.EMPTY
        self._action = Action.IDLE
        self._next_action = Action.IDLE
        self._next_value = 0.0
        self._target = Vector()
        self._held: Optional["Entity"] = None
        self._interactant: Optional["Entity"] = None
        self._max_stamina = self.stamina
        self._delay = clamp(Delay.MAX, Delay.MIN, Delay.MAX - self.recovery)

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

        self._target = self._partition.get_position_for_direction(
            math.floor(self.position.x),
            math.floor(self.position.y),
            math.floor(self.position.z),
            self.direction,
        )

        self._busy = True

    def _prepare_use(self) -> None:
        if self._held is None:
            return

        seconds_since_action = self._get_elapsed_seconds_since_action()

        if seconds_since_action < self._delay:
            return

        self._action = self._next_action
        self._busy = True

    def _prepare_destroy(self):
        self.density = Density.VOID
        self.position.z -= 1

        self._action = self._next_action
        self._busy = True

    def _prepare_take(self) -> None:
        if self._held is not None:
            return

        entities = cast(List["Entity"], self._partition.find_by_direction(self))
        if not entities:
            return

        entity = entities[-1]
        if entity.density != Density.SOLID:
            return
        if entity.visible is False:
            return

        self._held = entity
        self._held.density = Density.VOID
        self._held.state = State.HELD
        self._held.visible = not self._held.equippable

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

    def _prepare_interact(self):
        if self._interactant is not None:
            return

        interactant = None
        entities = cast(List["Entity"], self._partition.find_by_direction(self))

        for entity in entities:
            if entity.actuator is not None:
                interactant = entity
                break

        if interactant is None:
            return

        self._interactant = interactant
        self._interactant.actuator.prepare(interactee=self)

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
        elif self._next_action == Action.INTERACT:
            self._prepare_interact()

        self._timestmap_prepare = get_time_milliseconds()

    def _do_idle(self) -> None:
        self.state = State.IDLING
        self._busy = False

    def _do_move(self) -> None:
        self.state = State.MOVING

        surfaces = cast(List["Entity"], self._partition.find_by_position(self.position))
        friction = Density.SOLID - surfaces[0].density

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

    def _do_use_tool(self):
        if self._held.spawns != EntityType.EMPTY:
            self.spawn()

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()
        targets = cast(List["Entity"], self._partition.find_by_direction(self))

        for target in targets:
            if target.visible is False:
                continue
            if target is self._held:
                continue

            # Wear the target
            target.durability -= self._held.strength * seconds_since_prepare

            # Restore the target
            target.durability += self._held.durability * seconds_since_prepare
            target.stamina += self._held.stamina * seconds_since_prepare

    def _do_use(self) -> None:
        self.state = State.USING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare < self._delay:
            return

        self._do_use_tool()

        self._action = Action.IDLE
        self._busy = False
        self._timestamp_action = get_time_milliseconds()

    def _do_destroy(self):
        self.state = State.DESTROYING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare < Delay.MAX:
            return

        self.state = State.DESTROYED
        self._drop()

        self._busy = False

    def _do_take(self):
        self.state = State.TAKING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()
        ratio = self._held.weight / self.strength

        if seconds_since_prepare < self._delay * ratio:
            return

        self._action = Action.IDLE
        self._busy = False

    def _do_drop(self):
        self.state = State.DROPPING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()
        ratio = self._held.weight / self.strength

        if seconds_since_prepare < self._delay * ratio:
            return

        self._drop()

        self._action = Action.IDLE
        self._busy = False

    def _do_exhaust(self):
        self.state = State.EXHAUSTED

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare < self._delay * Penalty.MAX:
            return

        self._drop()

        # Interrupt the action provided by the client
        self.perform(Action.IDLE)
        self._busy = False

    def _do_interact(self):
        if self._interactant is None:
            return

        self.state = State.INTERACTING

        if self._interactant.actuator.finished() is False:
            return

        self.perform(Action.IDLE)
        self._interactant = None
        self._busy = False

    def _drop(self):
        if self._held is None:
            return

        self._held.visible = True
        self._held.density = Density.SOLID
        self._held.state = State.IDLING
        self._held = None

    def _reset_flags(self):
        self._spawned = EntityType.EMPTY

    def _check_attributes(self):
        if self.durability <= 0:
            self.perform(Action.DESTROY)
        if self.stamina <= 0:
            self.perform(Action.EXHAUST)

    def _check_in_blocking_state(self):
        return self.state in [
            State.DESTROYED,
            State.HELD,
        ]

    def _update_actuator(self) -> None:
        if self.actuator is not None:
            self.actuator.tick()

    def _update_stamina(self) -> None:
        seconds_since_tick = self._get_elapsed_seconds_since_tick()

        cost = self.__stamina_cost_by_action__.get(self._action, Cost.MIN)
        gain = abs(cost) * self.recovery
        delta = (gain - (cost - Cost.MIN)) * seconds_since_tick

        self.stamina = clamp(self._max_stamina, 0, self.stamina + delta)

    def _update_held(self):
        if self._held is None:
            return

        self._partition.remove(self._held)

        self._held.direction = self.direction
        self._held.position = self._partition.get_position_for_direction(
            self.position.x,
            self.position.y,
            self.position.z,
            self.direction,
        )

        self._partition.add(self._held)

    def tick(self) -> None:
        if self._check_in_blocking_state():
            return

        self._reset_flags()

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
        elif self._action == Action.INTERACT:
            self._do_interact()

        self._check_attributes()
        self._update_actuator()
        self._update_stamina()
        self._update_held()
        self._prepare_next_tick()

        self._timestamp_tick = get_time_milliseconds()

    def perform(self, action: Action, value: float = 0) -> None:
        self._next_action = action
        self._next_value = value

    def removed(self):
        return self.state == State.DESTROYED and self.removable is True

    def spawn(self):
        self._spawned = self.spawns

        if self._held is not None and self._held.spawns != EntityType.EMPTY:
            self._spawned = self._held.spawns

    def spawned(self):
        return self._spawned

    def spawned_at(self):
        position = Vector.new_for_position(self.position)

        if self._held is not None and self._held.spawns != EntityType.EMPTY:
            position = Vector.new_for_position(self._held.position)

        return position

    def targets(self) -> Optional["Entity"]:
        return self.__entity_by_name__.get(self.target)

    def teleport(self, position: Vector) -> None:
        self._partition.remove(self)

        self.position.x = position.x
        self.position.y = position.y
        self.position.z = position.z

        self._target = self._partition.get_position_for_direction(
            position.x,
            position.y,
            position.z,
            self.direction,
        )

        self._partition.add(self)

    def surroundings(self):
        surroundings = []

        entities = self._partition.find_by_distance(
            target=self,
            distance_x=self.radius,
            distance_y=self.radius,
        )

        for entity in entities:
            if entity.density == Density.SOLID:
                surroundings.append(entity)

        return surroundings

    @classmethod
    def new_with_name(cls, *args, **kargs) -> "Entity":
        entity = cls(*args, **kargs)

        if entity.name:
            cls.__entity_by_name__[entity.name] = entity

        return entity


class EntityRegistry:
    __entities__: Dict[int, Description] = {}

    @classmethod
    def register(cls, description: Description) -> None:
        cls.__entities__[description.id] = description

    @classmethod
    def find_and_override(
        cls,
        type_id: int,
        overrides: Optional[Description],
    ) -> Description:
        registry = cls.__entities__[type_id]
        description = deepcopy(registry.game.default)

        if overrides is not None:
            for attribute in vars(overrides):
                setattr(
                    description,
                    attribute,
                    getattr(overrides, attribute),
                )

        return description

    @classmethod
    def new_from_values(
        cls,
        id: int,
        type_id: int,
        position: Vector,
        overrides: Optional[Description],
        partition: SpatialPartition,
    ) -> Entity:
        description = cls.find_and_override(type_id=type_id, overrides=overrides)
        return Entity.new_with_name(
            id=id,
            type_id=type_id,
            position=position,
            stamina=description.stamina,
            durability=description.durability,
            weight=description.weight,
            strength=description.strength,
            recovery=description.recovery,
            removable=description.removable,
            equippable=description.equippable,
            density=description.density,
            visible=description.visible,
            spawns=description.spawns,
            name=description.name,
            actuator=description.actuator,
            target=description.target,
            radius=description.radius,
            rate=description.rate,
            direction=Direction[description.direction.upper()],
            state=State[description.state.upper()],
            partition=partition,
        )
