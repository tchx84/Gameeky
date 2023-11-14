import math

from typing import Optional

from gi.repository import GObject

from ...common.entity import Entity as CommonEntity
from ...common.scene import Scene as CommonScene
from ...common.scanner import Description
from ...common.vector import Vector
from ...common.definitions import EntityType, Direction, State

from ...server.game.entity import EntityRegistry


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        CommonScene.__init__(self, 0, 0)
        GObject.GObject.__init__(self)
        self._index = 0

    def _add(self, type_id: int, x: int, y: int, z: int) -> None:
        default = EntityRegistry.find(type_id).game.default

        entity = CommonEntity(
            id=self._index,
            type_id=type_id,
            position=Vector(x, y, z),
            visible=default.visible,
            luminance=default.luminance,
            direction=Direction[default.direction.upper()],
            state=State[default.state.upper()],
        )

        self.entities.append(entity)
        self._index += 1

    def _remove(self, x: int, y: int, z: int) -> None:
        entity = self.find(x, y, z)

        if entity is None:
            return

        self.entities.remove(entity)

    def add(self, type_id: int, x: int, y: int, z: int, area: int) -> None:
        from_range_x = math.floor(max(x - area, 0))
        to_range_x = math.floor(min(x + area + 1, self.width))

        from_range_y = math.floor(max(y - area, 0))
        to_range_y = math.floor(min(y + area + 1, self.height))

        for _y in range(from_range_y, to_range_y):
            for _x in range(from_range_x, to_range_x):
                self._add(type_id, _x, _y, z)

        self.refresh()

    def find(self, x: int, y: int, z: int) -> Optional[CommonEntity]:
        target = Vector(x, y, z)

        for entity in reversed(self.entities):
            if entity.position == target:
                return entity

        return None

    def remove(self, x: int, y: int, z: int, area: int) -> None:
        from_range_x = math.floor(max(x - area, 0))
        to_range_x = math.floor(min(x + area + 1, self.width))

        from_range_y = math.floor(max(y - area, 0))
        to_range_y = math.floor(min(y + area + 1, self.height))

        for _y in range(from_range_y, to_range_y):
            for _x in range(from_range_x, to_range_x):
                self._remove(_x, _y, z)

        self.refresh()

    def refresh(self) -> None:
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
