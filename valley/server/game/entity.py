import math

from copy import deepcopy
from typing import Dict, List, Optional, cast

from .definitions import Density, Recovery, Delay
from .partition import SpatialPartition

from .actuators.base import Actuator
from .actuators.grows import Actuator as GrowsActuator
from .actuators.portal_switch import Actuator as PortalSwitchActuator
from .actuators.teleports import Actuator as TeleportsActuator
from .actuators.rots import Actuator as RotsActuator
from .actuators.exhausts import Actuator as ExhaustsActuator
from .actuators.destroys import Actuator as DestroysActuator
from .actuators.consumable import Actuator as ConsumableActuator
from .actuators.moves import Actuator as MovesActuator
from .actuators.targets import Actuator as TargetsActuator
from .actuators.uses import Actuator as UsesActuator
from .actuators.takes import Actuator as TakesActuator

from .handlers.base import Handler
from .handlers.destroy import Handler as DestroyHandler
from .handlers.drop import Handler as DropHandler
from .handlers.exhaust import Handler as ExhaustHandler
from .handlers.idle import Handler as IdleHandler
from .handlers.interact import Handler as InteractHandler
from .handlers.move import Handler as MoveHandler
from .handlers.take import Handler as TakeHandler
from .handlers.use import Handler as UseHandler

from ...common.action import Action
from ...common.state import State
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.entity import Vector
from ...common.utils import clamp
from ...common.entity import EntityType
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    __entity_by_name__: Dict[str, "Entity"] = {}

    __actuator_by_name__ = {
        GrowsActuator.name: GrowsActuator,
        PortalSwitchActuator.name: PortalSwitchActuator,
        TeleportsActuator.name: TeleportsActuator,
        RotsActuator.name: RotsActuator,
        ExhaustsActuator.name: ExhaustsActuator,
        DestroysActuator.name: DestroysActuator,
        ConsumableActuator.name: ConsumableActuator,
        MovesActuator.name: MovesActuator,
        TargetsActuator.name: TargetsActuator,
        UsesActuator.name: UsesActuator,
        TakesActuator.name: TakesActuator,
    }

    def __init__(
        self,
        stamina: float,
        durability: float,
        weight: float,
        strength: float,
        recovery: float,
        removable: bool,
        equippable: bool,
        density: Density,
        spawns: EntityType,
        name: str,
        actuators: List[str],
        target: str,
        radius: int,
        rate: float,
        partition: SpatialPartition,
        *args,
        **kargs,
    ) -> None:
        super().__init__(*args, **kargs)
        self.strength = strength
        self.recovery = clamp(Recovery.MAX, Recovery.MIN, recovery)
        self.removable = removable
        self.equippable = equippable
        self.density = clamp(Density.SOLID, Density.VOID, density)
        self.spawns = spawns
        self.name = name
        self.actuators: List[Actuator] = []
        self.radius = radius
        self.rate = rate
        self.action = Action.IDLE

        self._target = target
        self._weight = weight
        self._durability = durability
        self._stamina = stamina
        self._max_durability = durability
        self._max_stamina = stamina

        self._partition = partition

        self._next_action = Action.IDLE
        self._next_value = 0.0

        self._spawned = EntityType.EMPTY
        self._destination = Vector()
        self._held: Optional["Entity"] = None
        self._delay = clamp(Delay.MAX, Delay.MIN, Delay.MAX - self.recovery)

        for actuator in actuators:
            if ActuatorClass := self.__actuator_by_name__.get(actuator):
                self.actuators.append(ActuatorClass(self))

        self._handlers: Dict[Action, Handler] = {}
        self._handlers[Action.DESTROY] = DestroyHandler(self)
        self._handlers[Action.DROP] = DropHandler(self)
        self._handlers[Action.EXHAUST] = ExhaustHandler(self)
        self._handlers[Action.IDLE] = IdleHandler(self)
        self._handlers[Action.INTERACT] = InteractHandler(self)
        self._handlers[Action.MOVE] = MoveHandler(self)
        self._handlers[Action.TAKE] = TakeHandler(self)
        self._handlers[Action.USE] = UseHandler(self)

        self._handler = self._handlers[Action.IDLE]

    def _prepare(self) -> None:
        if self._handler.busy is True:
            return

        handler = self._handlers[self._next_action]

        if handler.prepare(self._next_value) is False:
            handler = self._handlers[Action.IDLE]
            handler.prepare(self._next_value)

        self._handler = handler

    def _update_flags(self) -> None:
        self._spawned = EntityType.EMPTY

    def _update_actuators(self) -> None:
        for actuator in self.actuators:
            actuator.tick()

    def _update_held(self) -> None:
        if self.held is None:
            return

        self.held.direction = self.direction
        self.held.position = self.position_at(self.direction)

    def tick(self) -> None:
        self._update_flags()
        self._update_actuators()
        self._update_held()

        if self.blocked is True:
            return

        self._prepare()
        self._handler.tick()

    def perform(self, action: Action, value: float = 0) -> None:
        self._next_action = action
        self._next_value = value

    def drop(self) -> None:
        if self.held is None:
            return

        self.held.visible = True
        self.held.density = Density.SOLID
        self.held.state = State.IDLING
        self.held = None

    def spawn(self) -> None:
        self._spawned = self.spawns

        if self.held is not None and self.held.spawns != EntityType.EMPTY:
            self._spawned = self.held.spawns

    def position_at(self, direction: Direction) -> Vector:
        return self._partition.get_position_for_direction(self.position, direction)

    @property
    def blocked(self) -> bool:
        return self.state in [
            State.DESTROYED,
            State.HELD,
        ]

    @property
    def removed(self) -> bool:
        return self.state == State.DESTROYED and self.removable is True

    @property
    def spawned(self) -> EntityType:
        return self._spawned

    @property
    def spawned_at(self) -> Vector:
        position = self.position.copy()

        if self.held is not None and self.held.spawns != EntityType.EMPTY:
            position = self.held.position.copy()

        return position

    @property
    def target(self) -> Optional["Entity"]:
        return self.__entity_by_name__.get(self._target)

    @target.setter
    def target(self, target: Optional["Entity"]) -> None:
        self._target = target.name if target is not None else ""

    @property
    def held(self) -> Optional["Entity"]:
        return self._held

    @held.setter
    def held(self, held) -> None:
        self._held = held

    @property
    def delay(self) -> float:
        return self._delay

    @property
    def weight(self) -> float:
        weight = self._weight

        if self.held is not None:
            weight += self.held.weight

        return weight

    @property
    def position(self) -> Vector:
        return self._position

    @position.setter
    def position(self, position) -> None:
        self._partition.remove(self)

        self._position = position.copy()

        self._partition.add(self)

    @property
    def destination(self) -> Vector:
        return self._destination

    @destination.setter
    def destination(self, destination) -> None:
        self._destination.x = math.floor(destination.x)
        self._destination.y = math.floor(destination.y)
        self._destination.z = math.floor(destination.z)

    @property
    def durability(self) -> float:
        return self._durability

    @durability.setter
    def durability(self, durability) -> None:
        self._durability = clamp(self._max_durability, 0, durability)

    @property
    def stamina(self) -> float:
        return self._stamina

    @stamina.setter
    def stamina(self, stamina) -> None:
        self._stamina = clamp(self._max_stamina, 0, stamina)

    @property
    def obstacles(self) -> List["Entity"]:
        return cast(List["Entity"], self._partition.find_by_direction(self))

    @property
    def obstacle(self) -> Optional["Entity"]:
        for entity in self.obstacles:
            if entity.density == Density.SOLID:
                return entity

        return None

    @property
    def surface(self) -> Optional["Entity"]:
        surfaces = cast(List["Entity"], self._partition.find_by_position(self.position))

        if not surfaces:
            return None

        return surfaces[0]

    @property
    def surroundings(self) -> List["Entity"]:
        surroundings = []

        entities = cast(
            List["Entity"],
            self._partition.find_by_distance(
                target=self,
                distance_x=self.radius,
                distance_y=self.radius,
            ),
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
            actuators=description.actuators,
            target=description.target,
            radius=description.radius,
            rate=description.rate,
            direction=Direction[description.direction.upper()],
            state=State[description.state.upper()],
            partition=partition,
        )
