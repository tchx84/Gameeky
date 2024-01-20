# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import math

from typing import Optional, List, cast

from gi.repository import GObject

from .entity import Entity

from ...common.scene import Scene as CommonScene
from ...common.scanner import Description
from ...common.vector import Vector
from ...common.definitions import DayTime, TILES_X, TILES_Y
from ...common.utils import valid_file
from ...common.config import VERSION

from ...server.game.partition import SpatialPartition


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        CommonScene.__init__(self, 0, 0)
        GObject.GObject.__init__(self)
        self._index = 0
        self._partition: Optional[SpatialPartition] = None
        self._name = ""
        self.spawn = Vector()
        self.daytime = DayTime.DYNAMIC.name.lower()
        self.layer: Optional[int] = None

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
        index = len(self.entities)

        # Don't stack the same entity on the same position
        if type_id in [e.type_id for e in entities]:
            return

        # Force layer if specified
        if self.layer is not None:
            z = self.layer

        # Force removal of entity at layer if specified
        if self.layer is not None and (replaced := self.find(x, y)):
            index = self.entities.index(replaced)
            self._remove_entity(replaced)

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

        self.entities.insert(index, entity)
        self._partition.add(entity, self.layer)
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

    def remove_by_type_id(self, type_id: int) -> None:
        for entity in list(self.entities):
            if entity.type_id == type_id:
                self._remove_entity(cast(Entity, entity))

        self.refresh()

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

        # If specified loo for an entity at this layer
        for entity in entities:
            if entity.position.z == self.layer:
                return entity

        # If specified it should have returned already so don't return the wrong one
        if self.layer is not None:
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
        self.emit("updated")

    def reset(self) -> None:
        self._index = 0
        self.time = 0.0

        for entity in cast(List[Entity], list(self.entities)):
            self._remove_entity(entity)

    @property
    def name(self) -> str:
        return self._name if self._name else "Untitled"

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def ratio(self) -> float:
        return self.width / self.height

    @property
    def description(self) -> Description:
        return Description(
            name=self.name,
            version=VERSION,
            width=self.width,
            height=self.height,
            spawn=Description(
                x=self.spawn.x,
                y=self.spawn.y,
                z=self.spawn.z,
            ),
            daytime=self.daytime,
            entities=[cast(Entity, e).summary for e in self.entities],
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.reset()

        self._partition = SpatialPartition(description.width, description.height)

        self.name = description.name
        self.width = description.width
        self.height = description.height
        self.daytime = description.daytime

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

    @classmethod
    def new_from_file(cls, project_path: str, scene_path: str) -> Description:
        scene_path = os.path.join(project_path, scene_path)

        if valid_file(scene_path):
            return Description.new_from_json(scene_path)

        return Description(
            name="default",
            width=TILES_X * 2,
            height=TILES_Y * 2,
            spawn=Vector(),
            daytime=DayTime.DYNAMIC.name.lower(),
            entities=[],
        )
