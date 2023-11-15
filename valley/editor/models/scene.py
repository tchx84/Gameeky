import math

from typing import Optional, List, cast

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
        self._overrides: Optional[Description] = None

    def rotate(self) -> None:
        directions = list(Direction)
        index = directions.index(self.direction)
        direction = directions[(index + 1) % len(directions)]

        description = self.description
        description.direction = direction.name.lower()
        self.overrides = description

    @property
    def description(self) -> Description:
        if self._overrides is not None:
            return self._overrides

        return EntityRegistry.find(self.type_id).game.default

    @property
    def overrides(self) -> Optional[Description]:
        return self._overrides

    @overrides.setter
    def overrides(self, overrides: Description) -> None:
        self.visible = overrides.visible
        self.luminance = overrides.luminance
        self.state = State[overrides.state.upper()]
        self.direction = Direction[overrides.direction.upper()]

        self._overrides = overrides
        self.emit("changed")


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        CommonScene.__init__(self, 0, 0)
        GObject.GObject.__init__(self)
        self._index = 0
        self._partition: Optional[SpatialPartition] = None

    def _add(self, type_id: int, x: int, y: int, z: Optional[int]) -> None:
        if self._partition is None:
            return

        position = Vector(x, y)
        entities = cast(List[Entity], self._partition.find_by_position(position))

        # Don't stack the same entity on the same position
        if type_id in [e.type_id for e in entities]:
            return

        # If not specified then calculate depth value
        position.z = z if z is not None else len(entities)

        default = EntityRegistry.find(type_id).game.default
        entity = Entity(
            id=self._index,
            type_id=type_id,
            position=position,
            visible=default.visible,
            luminance=default.luminance,
            direction=Direction[default.direction.upper()],
            state=State[default.state.upper()],
        )

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

    def find(self, x: int, y: int) -> Optional[Entity]:
        if self._partition is None:
            return None

        position = Vector(x, y)
        entities = cast(List[Entity], self._partition.find_by_position(position))

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
        return Description()

    @description.setter
    def description(self, description: Description) -> None:
        self.time = 0.0
        self.width = description.width
        self.height = description.height
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

                self.add(type_id, x, y, z, 0)
