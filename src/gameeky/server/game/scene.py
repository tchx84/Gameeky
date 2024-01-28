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

import math

from typing import List, Dict, Optional

from gi.repository import GLib

from .partition import SpatialPartition
from .entity import Entity, EntityRegistry

from ...common.logger import logger
from ...common.vector import Vector
from ...common.scanner import Description
from ...common.definitions import Action, EntityType, DayTime, TICK, TILES_X, TILES_Y
from ...common.scene import Scene as CommonScene
from ...common.stats import Stats as CommonStats
from ...common.utils import get_time_milliseconds, add_timeout_source, remove_source_id


class Scene:
    def __init__(
        self,
        name: str,
        width: int,
        height: int,
        spawn: Vector,
        daytime: DayTime,
        duration: int,
    ) -> None:
        self._time = 0.0
        self._index = 0
        self._mutable_entities: List[Entity] = []
        self._playable_entities: List[Entity] = []
        self._entity_by_id: Dict[int, Entity] = {}
        self._entity_by_name: Dict[str, Entity] = {}
        self._partition = SpatialPartition(width=width, height=height)

        self.name = name
        self.width = width
        self.height = height
        self.spawn = spawn
        self.daytime = daytime
        self.duration = duration

        self._timeout_source_id: Optional[int] = add_timeout_source(
            TICK,
            self.__on_scene_ticked,
        )

    def __on_scene_ticked(self, *args) -> int:
        self.tick()
        return GLib.SOURCE_CONTINUE

    def _tick_time(self) -> None:
        if self.daytime == DayTime.DAY:
            self._time = 0.0
        elif self.daytime == DayTime.NIGHT:
            self._time = 1.0
        else:
            self._time = get_time_milliseconds() / 1000 / self.duration

    def tick(self) -> None:
        added = []
        removed = []

        for entity in self._mutable_entities:
            entity.tick()

            if entity.removed:
                removed.append(entity)
            if entity.spawned:
                added.append(entity)

        for entity in removed:
            self.remove(entity.id)

        for entity in added:
            self.add(
                entity.spawned,
                entity.spawned_at,
                Description(direction=entity.direction.name),
            )

        self._tick_time()

    def add(
        self,
        type_id: int,
        position: Vector,
        overrides: Optional[Description] = None,
    ) -> Entity:
        entity = EntityRegistry.new_from_values(
            id=self._index,
            type_id=type_id,
            position=position,
            overrides=overrides,
            scene=self,
        )

        self._index += 1
        self._entity_by_id[entity.id] = entity
        self._partition.add(entity)

        if entity.name:
            self._entity_by_name[entity.name] = entity

        if entity.mutable or entity.playable:
            self._mutable_entities.append(entity)

        if entity.playable:
            self._playable_entities.append(entity)

        return entity

    def update(self, entity_id: int, action: Action, value: float) -> None:
        entity = self._entity_by_id[entity_id]
        entity.perform(action, value)

    def remove(self, entity_id: int) -> None:
        entity = self._entity_by_id[entity_id]
        entity.drop()

        del self._entity_by_id[entity_id]
        self._partition.remove(entity)
        entity.shutdown()

        if self._entity_by_name.get(entity.name) == entity:
            del self._entity_by_name[entity.name]

        if entity.mutable is True:
            self._mutable_entities.remove(entity)

        if entity.playable is True:
            self._playable_entities.remove(entity)

    def prepare_for_entity_id(self, entity_id: int) -> CommonScene:
        entity = self._entity_by_id[entity_id]

        x = TILES_X / 2
        y = TILES_Y / 2

        distance_x = math.ceil(x) if entity.horizontally else math.floor(x)
        distance_y = math.ceil(y) if entity.vertically else math.floor(y)

        entities = self._partition.find_by_distance(
            target=entity,
            distance_x=distance_x,
            distance_y=distance_y,
        )

        return CommonScene(
            time=self._time,
            width=TILES_X,
            height=TILES_Y,
            anchor=entity.position,
            entities=entities,
        )

    def prepare_stats_for_entity_id(self, entity_id: int) -> CommonStats:
        entity = self._entity_by_id[entity_id]
        held = entity.held.type_id if entity.held is not None else EntityType.EMPTY

        return CommonStats(
            durability=entity.normalized_durability,
            stamina=entity.normalized_stamina,
            held=held,
        )

    def find_by_id(self, id: int) -> Optional[Entity]:
        return self._entity_by_id.get(id)

    def find_by_name(self, name: str) -> Optional[Entity]:
        return self._entity_by_name.get(name)

    def shutdown(self) -> None:
        if self._timeout_source_id is not None:
            remove_source_id(self._timeout_source_id)

        self._timeout_source_id = None

        logger.debug("Server.Scene.shut")

    @property
    def partition(self) -> SpatialPartition:
        return self._partition

    @property
    def entities(self) -> List[Entity]:
        return list(self._entity_by_id.values())

    @property
    def mutables(self) -> List[Entity]:
        return self._mutable_entities

    @property
    def playables(self) -> List[Entity]:
        return self._playable_entities

    @property
    def description(self) -> Description:
        spawn = self.spawn.copy()
        entities: List[Description] = []

        for entity in self.entities:
            if entity.playable:
                spawn = entity.position.copy()
            else:
                entities.append(entity.description)

        return Description(
            name=self.name,
            width=self.width,
            height=self.height,
            spawn=Description(
                x=spawn.x,
                y=spawn.y,
                z=spawn.z,
            ),
            daytime=self.daytime.name.lower(),
            duration=self.duration,
            entities=entities,
        )

    @classmethod
    def new_from_description(cls, description: Description) -> "Scene":
        scene = cls(
            name=description.name,
            width=description.width,
            height=description.height,
            spawn=Vector(
                x=description.spawn.x,
                y=description.spawn.y,
                z=description.spawn.z,
            ),
            daytime=DayTime[description.daytime.upper()],
            duration=description.duration,
        )

        for entity in description.entities:
            scene.add(
                type_id=entity.type_id,
                position=Vector(
                    x=entity.position.x,
                    y=entity.position.y,
                    z=entity.position.z,
                ),
                overrides=entity.overrides,
            )

        return scene
