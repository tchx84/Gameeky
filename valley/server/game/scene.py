import math

from typing import List, Dict, Optional

from gi.repository import GLib

from .partition import SpatialPartition
from .entity import Entity, EntityRegistry

from ...common.logger import logger
from ...common.vector import Vector
from ...common.scanner import Description
from ...common.definitions import Action, EntityType, TICK, TILES_X, TILES_Y
from ...common.scene import Scene as CommonScene
from ...common.stats import Stats as CommonStats
from ...common.utils import get_time_milliseconds, add_timeout_source, remove_source_id


class Scene:
    def __init__(self, name: str, width: int, height: int, spawn: Vector) -> None:
        self._time = 0.0
        self._index = 0
        self._mutable_entities: List[Entity] = []
        self._entity_by_id: Dict[int, Entity] = {}
        self._partition = SpatialPartition(width=width, height=height)

        self.name = name
        self.width = width
        self.height = height
        self.spawn = spawn

        self._timeout_source_id: Optional[int] = add_timeout_source(
            TICK,
            self.__on_scene_ticked,
        )

    def __on_scene_ticked(self, *args) -> int:
        self.tick()
        return GLib.SOURCE_CONTINUE

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

        # A full day in one hour
        self._time = get_time_milliseconds() / 1000 / 60 / 60

    def add(
        self,
        type_id: int,
        position: Vector,
        overrides: Optional[Description] = None,
    ) -> int:
        entity = EntityRegistry.new_from_values(
            id=self._index,
            type_id=type_id,
            position=position,
            overrides=overrides,
            partition=self._partition,
        )

        self._index += 1
        self._entity_by_id[entity.id] = entity
        self._partition.add(entity)

        if entity.mutable is True:
            self._mutable_entities.append(entity)

        return entity.id

    def update(self, entity_id: int, action: Action, value: float) -> None:
        entity = self._entity_by_id[entity_id]
        entity.perform(action, value)

    def remove(self, entity_id: int) -> None:
        entity = self._entity_by_id[entity_id]
        entity.drop()

        del self._entity_by_id[entity_id]
        self._partition.remove(entity)
        Entity.unregister(entity)

        if entity.mutable is True:
            self._mutable_entities.remove(entity)

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

    def shutdown(self) -> None:
        if self._timeout_source_id is not None:
            remove_source_id(self._timeout_source_id)

        self._timeout_source_id = None

        logger.info("Server.Scene.shut")

    @property
    def entities(self):
        return list(self._entity_by_id.values())

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
