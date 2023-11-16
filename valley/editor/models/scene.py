import math

from typing import Dict, Optional, List, cast

from gi.repository import GObject

from ...common.entity import Entity as CommonEntity
from ...common.scene import Scene as CommonScene
from ...common.scanner import Description
from ...common.vector import Vector
from ...common.definitions import EntityType, Direction, State

from ...server.game.partition import SpatialPartition
from ...server.game.entity import EntityRegistry


class Entity(CommonEntity, GObject.GObject):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, *args, **kargs) -> None:
        CommonEntity.__init__(self, *args, **kargs)
        GObject.GObject.__init__(self)
        self._description = Description()

    def reset(self) -> None:
        self.description = self.defaults

    def rotate(self) -> None:
        directions = list(Direction)
        index = directions.index(self.direction)
        direction = directions[(index + 1) % len(directions)]

        self.direction = direction
        self._description.direction = direction.name.lower()
        self.emit("changed")

    @property
    def defaults(self) -> Description:
        return EntityRegistry.find(self.type_id).game.default

    @property
    def description(self) -> Description:
        return self._description

    @description.setter
    def description(self, description: Description) -> None:
        _description = description.__dict__

        for key in _description:
            setattr(self._description, key, _description[key])

        for key in self.__dict__:
            if key not in _description:
                continue

            value = _description[key]

            if key == "state":
                value = State[value.upper()]
            elif key == "direction":
                value = Direction[value.upper()]

            setattr(self, key, value)

        self.emit("changed")

    @property
    def delta(self) -> Optional[Description]:
        description = self.description.__dict__
        defaults = self.defaults.__dict__
        delta = {
            k: description[k] for k in description if description[k] != defaults[k]
        }

        if not delta:
            return None

        return Description(**delta)


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        CommonScene.__init__(self, 0, 0)
        GObject.GObject.__init__(self)
        self._index = 0
        self._partition: Optional[SpatialPartition] = None
        self.spawn = Vector()

    def _add(
        self,
        type_id: int,
        x: int,
        y: int,
        z: Optional[int],
        overrides: Optional[Description] = None,
    ) -> None:
        if self._partition is None:
            return

        position = Vector(x, y)
        entities = cast(List[Entity], self._partition.find_by_position(position))

        # Don't stack the same entity on the same position
        if type_id in [e.type_id for e in entities]:
            return

        # If not specified then calculate depth value
        position.z = z if z is not None else len(entities)

        entity = Entity(
            id=self._index,
            type_id=type_id,
            position=position,
        )
        entity.reset()

        if overrides is not None:
            entity.description = overrides

        entity.connect("changed", self.refresh)

        self.entities.append(entity)
        self._partition.add(entity)
        self._index += 1

    def _remove(self, x: int, y: int) -> None:
        if self._partition is None:
            return

        entity = self.find(x, y)

        if entity is None:
            return

        entity.disconnect_by_func(self.refresh)

        self.entities.remove(entity)
        self._partition.remove(entity)

    def add(self, type_id: int, x: int, y: int, z: Optional[int], area: int) -> None:
        from_range_x = math.floor(max(x - area, 0))
        to_range_x = math.floor(min(x + area + 1, self.width))

        from_range_y = math.floor(max(y - area, 0))
        to_range_y = math.floor(min(y + area + 1, self.height))

        for _y in range(from_range_y, to_range_y):
            for _x in range(from_range_x, to_range_x):
                self._add(type_id, _x, _y, z)

        self.refresh()

    def find_all(self, x: int, y: int) -> List[Entity]:
        if self._partition is None:
            return []

        position = Vector(x, y)
        return cast(List[Entity], self._partition.find_by_position(position))

    def find(self, x: int, y: int) -> Optional[Entity]:
        entities = self.find_all(x, y)

        if not entities:
            return None

        return entities[-1]

    def remove(self, x: int, y: int, area: int) -> None:
        from_range_x = math.floor(max(x - area, 0))
        to_range_x = math.floor(min(x + area + 1, self.width))

        from_range_y = math.floor(max(y - area, 0))
        to_range_y = math.floor(min(y + area + 1, self.height))

        for _y in range(from_range_y, to_range_y):
            for _x in range(from_range_x, to_range_x):
                self._remove(_x, _y)

        self.refresh()

    def refresh(self, *args) -> None:
        self.emit("ticked")

    @property
    def ratio(self) -> float:
        return self.width / self.height

    @property
    def description(self) -> Description:
        description = Description(
            width=self.width,
            height=self.height,
            spawn=Description(
                x=self.spawn.x,
                y=self.spawn.y,
                z=self.spawn.z,
            ),
            layers=[],
            overrides=Description(),
        )

        if self._partition is None:
            return description

        layers: Dict[str, Description] = {}
        overrides: Dict[str, Description] = {}
        depth = 0 if not self.entities else max([e.position.z for e in self.entities])

        # Fill all layers with zeroes
        for depth in range(0, int(depth) + 1):
            for row in range(0, self.height):
                for column in range(0, self.width):
                    name = str(depth)
                    layer = layers.get(name, Description(name=name, entities=[]))
                    layer.entities.append(EntityType.EMPTY)
                    layers[name] = layer

        # Replace empty cells with existing entities
        for entity in self.entities:
            name = str(entity.position.z)
            index = (entity.position.y * self.width) + entity.position.x

            layer = layers.get(name, Description(name=name, entities=[]))
            layer.entities[index] = entity.type_id

            # Detect overrides
            delta = cast(Entity, entity).delta

            if not delta:
                continue

            override = overrides.get(name, Description())

            key = f"{entity.position.x}_{entity.position.y}"
            setattr(override, key, delta)

            overrides[name] = override

        for layer in layers.values():
            description.layers.append(layer)

        description.overrides = Description(**overrides)

        return description

    @description.setter
    def description(self, description: Description) -> None:
        self.time = 0.0
        self.width = description.width
        self.height = description.height
        self.spawn = Vector(
            x=description.spawn.x,
            y=description.spawn.y,
            z=description.spawn.z,
        )
        self._partition = SpatialPartition(self.width, self.height)

        # XXX figure out where the 0.5 offset is coming from
        self.anchor = Vector(
            x=math.floor(self.width / 2) - 0.5,
            y=math.floor(self.height / 2),
        )

        for depth, layer in enumerate(description.layers):
            for index, type_id in enumerate(layer.entities):
                if type_id == EntityType.EMPTY:
                    continue

                x = index % self.width
                y = int(index / self.width)
                z = depth

                overrides = getattr(description.overrides, str(depth), Description())
                overrides = getattr(overrides, f"{x}_{y}", None)

                self._add(type_id, x, y, z, overrides)
