import math

from copy import deepcopy
from typing import Dict, List, Optional, cast

from .definitions import Density, Recovery, Delay
from .partition import SpatialPartition

from .actuators.base import Actuator, ActuatorRegistry
from .actuators.transmutes import Actuator as TransmutesActuator
from .actuators.teleports import Actuator as TeleportsActuator
from .actuators.teleports_i import Actuator as TeleportsIActuator
from .actuators.deteriorates import Actuator as DeterioratesActuator
from .actuators.exhausts import Actuator as ExhaustsActuator
from .actuators.destroys import Actuator as DestroysActuator
from .actuators.destroys_i import Actuator as DestroysIActuator
from .actuators.follows import Actuator as FollowsActuator
from .actuators.roams import Actuator as RoamsActuator
from .actuators.targets import Actuator as TargetsActuator
from .actuators.uses import Actuator as UsesActuator
from .actuators.takes import Actuator as TakesActuator
from .actuators.interacts import Actuator as InteractsActuator
from .actuators.spawns import Actuator as SpawnsActuator
from .actuators.drops import Actuator as DropsActuator
from .actuators.triggers import Actuator as TriggersActuator
from .actuators.triggers_i import Actuator as TriggersIActuator
from .actuators.requires import Actuator as RequiresActuator
from .actuators.activates import Actuator as ActivatesActuator
from .actuators.activates_i import Actuator as ActivatesIActuator
from .actuators.propulses import Actuator as PropulsesActuator
from .actuators.collapses import Actuator as CollapsesActuator
from .actuators.collapses_t import Actuator as CollapsesTActuator
from .actuators.affects import Actuator as AffectsActuator
from .actuators.affects_i import Actuator as AffectsIActuator
from .actuators.aggroes import Actuator as AggroesActuator

from .handlers.base import Handler
from .handlers.destroy import Handler as DestroyHandler
from .handlers.drop import Handler as DropHandler
from .handlers.exhaust import Handler as ExhaustHandler
from .handlers.idle import Handler as IdleHandler
from .handlers.interact import Handler as InteractHandler
from .handlers.move import Handler as MoveHandler
from .handlers.take import Handler as TakeHandler
from .handlers.use import Handler as UseHandler

from ...common.scanner import Description
from ...common.vector import Vector
from ...common.utils import clamp, division, element
from ...common.definitions import Action, Direction, EntityType, State
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    __entity_by_name__: Dict[str, "Entity"] = {}

    __handler_by_action__ = {
        Action.DESTROY: DestroyHandler,
        Action.DROP: DropHandler,
        Action.EXHAUST: ExhaustHandler,
        Action.IDLE: IdleHandler,
        Action.INTERACT: InteractHandler,
        Action.MOVE: MoveHandler,
        Action.TAKE: TakeHandler,
        Action.USE: UseHandler,
    }

    __actuator_by_name__ = {
        TransmutesActuator.name: TransmutesActuator,
        TeleportsActuator.name: TeleportsActuator,
        TeleportsIActuator.name: TeleportsIActuator,
        DeterioratesActuator.name: DeterioratesActuator,
        ExhaustsActuator.name: ExhaustsActuator,
        DestroysActuator.name: DestroysActuator,
        DestroysIActuator.name: DestroysIActuator,
        FollowsActuator.name: FollowsActuator,
        RoamsActuator.name: RoamsActuator,
        TargetsActuator.name: TargetsActuator,
        UsesActuator.name: UsesActuator,
        TakesActuator.name: TakesActuator,
        InteractsActuator.name: InteractsActuator,
        SpawnsActuator.name: SpawnsActuator,
        DropsActuator.name: DropsActuator,
        TriggersActuator.name: TriggersActuator,
        TriggersIActuator.name: TriggersIActuator,
        RequiresActuator.name: RequiresActuator,
        ActivatesActuator.name: ActivatesActuator,
        ActivatesIActuator.name: ActivatesIActuator,
        PropulsesActuator.name: PropulsesActuator,
        CollapsesActuator.name: CollapsesActuator,
        CollapsesTActuator.name: CollapsesTActuator,
        AffectsActuator.name: AffectsActuator,
        AffectsIActuator.name: AffectsIActuator,
        AggroesActuator.name: AggroesActuator,
    }

    def __init__(
        self,
        stamina: float,
        durability: float,
        weight: float,
        strength: float,
        recovery: float,
        removable: bool,
        takeable: bool,
        usable: bool,
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
        self.takeable = takeable
        self.usable = usable
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
        self._default_density = density
        self._default_visible = self.visible

        self._partition = partition

        self._next_action = Action.IDLE
        self._next_value = 0.0

        self._held: Optional["Entity"] = None
        self._held_by: Optional["Entity"] = None

        self._spawned = EntityType.EMPTY
        self._destination = Vector()
        self._delay = clamp(Delay.MAX, Delay.MIN, Delay.MAX - self.recovery)
        self._handlers: Dict[Action, Handler] = {}

        for action, HandlerClass in self.__handler_by_action__.items():
            self._handlers[action] = HandlerClass(self)

        self._handler = self._handlers[Action.IDLE]

        for actuator in actuators:
            if ActuatorClass := self.__actuator_by_name__.get(actuator):
                self.actuators.append(ActuatorClass(self))
            elif ActuatorClass := ActuatorRegistry.find(actuator):
                self.actuators.append(ActuatorClass(self))

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

        if self.obstacle is not None:
            return

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

    def stop(self) -> None:
        self._handler.cancel()

    def activate(self) -> None:
        for actuator in self.actuators:
            if actuator.activatable is True:
                actuator.activate()

    def drop(self, state: Optional[State] = None) -> None:
        if self.held is None:
            return

        if state is not None:
            self.held.state = state

        self.held.secure()
        self.held.restore()
        self.held = None

    def fall(self) -> None:
        if self.held_by is not None:
            self.held_by.drop()

    def spawn(self) -> None:
        self._spawned = self.spawns

        if self.held is not None and self.held.spawns != EntityType.EMPTY:
            self._spawned = self.held.spawns

    def position_at(self, direction: Direction) -> Vector:
        return self._partition.get_position_for_direction(self.position, direction)

    def secure(self) -> None:
        self.position = Vector(
            math.floor(self.position.x),
            math.floor(self.position.y),
            math.floor(self.position.z),
        )

    def restore(self) -> None:
        self.visible = self._default_visible
        self.density = self._default_density

    @property
    def horizontally(self) -> bool:
        return self.direction in [Direction.EAST, Direction.WEST]

    @property
    def vertically(self) -> bool:
        return self.direction in [Direction.SOUTH, Direction.NORTH]

    @property
    def busy(self) -> bool:
        return self._handler.busy

    @property
    def mutable(self) -> bool:
        return len(self.actuators) > 0 or self.type_id == EntityType.PLAYER

    @property
    def interactable(self) -> bool:
        for actuator in self.actuators:
            if actuator.interactable is True:
                return True

        return False

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
        position = self.position

        if self.held is not None and self.held.spawns != EntityType.EMPTY:
            position = self.held.position

        return position.copy()

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
    def held(self, held: Optional["Entity"]) -> None:
        # Unset reference from the previous held entity
        if self._held is not None:
            self._held.held_by = None

        # Set reference to the new held entity
        if held is not None:
            held.held_by = self

        self._held = held

    @property
    def held_by(self) -> Optional["Entity"]:
        return self._held_by

    @held_by.setter
    def held_by(self, held_by: Optional["Entity"]) -> None:
        self._held_by = held_by

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
        self.status = self.normalized_durability

    @property
    def stamina(self) -> float:
        return self._stamina

    @stamina.setter
    def stamina(self, stamina) -> None:
        self._stamina = clamp(self._max_stamina, 0, stamina)

    @property
    def normalized_durability(self) -> float:
        return division(self._durability, self._max_durability)

    @property
    def normalized_stamina(self) -> float:
        return division(self._stamina, self._max_stamina)

    @property
    def obstacles(self) -> List["Entity"]:
        return cast(List["Entity"], self._partition.find_by_direction(self))

    @property
    def obstacle(self) -> Optional["Entity"]:
        obstacles = []

        for obstacle in self.obstacles:
            if obstacle.density == Density.SOLID:
                obstacles.append(obstacle)

        return element(obstacles, -1)

    @property
    def surfaces(self) -> List["Entity"]:
        return cast(List["Entity"], self._partition.find_by_position(self.position))

    @property
    def surface(self) -> Optional["Entity"]:
        return element(self.surfaces, 0)

    @property
    def overlay(self) -> Optional["Entity"]:
        return element(self.surfaces, -1)

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

    @classmethod
    def unregister(cls, entity: "Entity") -> None:
        if cls.__entity_by_name__.get(entity.name) == entity:
            del cls.__entity_by_name__[entity.name]


class EntityRegistry:
    __entities__: Dict[int, Description] = {}

    @classmethod
    def reset(cls) -> None:
        cls.__entities__ = {}

    @classmethod
    def register(cls, description: Description) -> None:
        cls.__entities__[description.id] = description

    @classmethod
    def find(cls, type_id: int) -> Description:
        return cls.__entities__[type_id]

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
            takeable=description.takeable,
            usable=description.usable,
            density=description.density,
            visible=description.visible,
            spawns=description.spawns,
            name=description.name,
            actuators=description.actuators,
            target=description.target,
            radius=description.radius,
            rate=description.rate,
            luminance=description.luminance,
            direction=Direction[description.direction.upper()],
            state=State[description.state.upper()],
            partition=partition,
        )
