import math

from typing import Dict, Optional

from gi.repository import GLib

from .partition import SpatialPartition
from .entity import Entity, EntityRegistry

from ...common.action import Action
from ...common.entity import EntityType, Vector
from ...common.scanner import Description
from ...common.definitions import TICK, TILES_X, TILES_Y
from ...common.scene import Scene as CommonScene


class Scene:
    def __init__(self, width: int, height: int, spawn: Vector) -> None:
        self._index = 0
        self._entity_by_id: Dict[int, Entity] = {}
        self._partition = SpatialPartition(width=width, height=height)

        self.width = width
        self.height = height
        self.spawn = spawn

        GLib.timeout_add(TICK, self.__on_scene_ticked)

    def __on_scene_ticked(self) -> int:
        self.tick()
        return GLib.SOURCE_CONTINUE

    def tick(self) -> None:
        added = []
        removed = []

        for entity in self._entity_by_id.values():
            if entity.mutable is False:
                continue

            entity.tick()

            if entity.removed:
                removed.append(entity)
            if entity.spawned:
                added.append(entity)

        for entity in removed:
            self.remove(entity.id)

        for entity in added:
            self.add(entity.spawned, entity.spawned_at)

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

        return entity.id

    def update(self, entity_id: int, action: Action, value: float) -> None:
        entity = self._entity_by_id[entity_id]
        entity.perform(action, value)

    def remove(self, entity_id: int) -> None:
        entity = self._entity_by_id[entity_id]

        del self._entity_by_id[entity_id]
        self._partition.remove(entity)

    def prepare_for_entity_id(self, entity_id: int) -> CommonScene:
        entity = self._entity_by_id[entity_id]
        distance_x = math.floor(TILES_X / 2)
        distance_y = math.floor(TILES_Y / 2)

        entities = self._partition.find_by_distance(
            target=entity,
            distance_x=distance_x,
            distance_y=distance_y,
        )

        return CommonScene(
            width=TILES_X,
            height=TILES_Y,
            anchor=entity.position,
            entities=entities,
        )

    @property
    def entities(self):
        return list(self._entity_by_id.values())

    @classmethod
    def new_from_description(cls, description: Description) -> "Scene":
        scene = cls(
            width=description.width,
            height=description.height,
            spawn=Vector(
                x=description.spawn.x,
                y=description.spawn.y,
                z=description.spawn.z,
            ),
        )

        for depth, layer in enumerate(description.layers):
            for index, type_id in enumerate(layer.entities):
                if type_id == EntityType.EMPTY:
                    continue

                position = Vector()
                position.x = index % scene.width
                position.y = int(index / scene.width)
                position.z = depth

                # XXX Remove these hacks when format and classes are set
                overrides = getattr(description.overrides, layer.name, Description())
                overrides = getattr(overrides, f"{position.x}_{position.y}", None)

                scene.add(type_id, position, overrides)

        return scene
