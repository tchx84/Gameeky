import math

from typing import Optional, List, cast

from gi.repository import GObject

from .entity import Entity

from ...common.scene import Scene as CommonScene
from ...common.scanner import Description
from ...common.vector import Vector

from ...server.game.partition import SpatialPartition


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

    def _remove_entity(self, entity: Entity) -> None:
        if self._partition is None:
            return

        entity.disconnect_by_func(self.refresh)

        self.entities.remove(entity)
        self._partition.remove(entity)

    def _remove(self, x: int, y: int) -> None:
        if self._partition is None:
            return

        entity = self.find(x, y)

        if entity is None:
            return

        self._remove_entity(entity)

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

    def reset(self) -> None:
        self._index = 0
        self.time = 0.0

        for entity in cast(List[Entity], list(self.entities)):
            self._remove_entity(entity)

    @property
    def ratio(self) -> float:
        return self.width / self.height

    @property
    def description(self) -> Description:
        return Description(
            width=self.width,
            height=self.height,
            spawn=Description(
                x=self.spawn.x,
                y=self.spawn.y,
                z=self.spawn.z,
            ),
            entities=[cast(Entity, e).summary for e in self.entities],
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.reset()

        self._partition = SpatialPartition(description.width, description.height)

        self.width = description.width
        self.height = description.height

        self.spawn = Vector(
            x=description.spawn.x,
            y=description.spawn.y,
            z=description.spawn.z,
        )

        for entity in description.entities:
            self._add(
                entity.type_id,
                entity.position.x,
                entity.position.y,
                entity.position.z,
                entity.overrides,
            )

        self.anchor = Vector(
            x=math.floor(self.width / 2) - (0 if self.width % 2 else 0.5),
            y=math.floor(self.height / 2) - (0 if self.height % 2 else 0.5),
        )
