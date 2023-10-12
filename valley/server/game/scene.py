import math

from typing import Dict

from gi.repository import GLib, GObject

from .entity import Entity, EntityRegistry

from ...common.action import Action
from ...common.entity import EntityType, Vector
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.definitions import TICK, TILES_X, TILES_Y
from ...common.scene import Scene as CommonScene


class Scene(CommonScene, GObject.GObject):
    def __init__(self, width: int, height: int) -> None:
        CommonScene.__init__(self, width, height)
        GObject.GObject.__init__(self)

        self._index = 0
        self._entity_by_id: Dict[int, Entity] = {}

        GLib.timeout_add(TICK, self.__on_scene_ticked)

    def __on_scene_ticked(self) -> int:
        self.tick()
        return GLib.SOURCE_CONTINUE

    def tick(self):
        for entity in self._entity_by_id.values():
            if entity.action == Action.IDLE:
                entity.idle()
            if entity.action == Action.MOVE:
                entity.move()

    def add(self, type_id: int, position: Vector) -> int:
        entity = EntityRegistry.new_from_values(
            id=self._index,
            type_id=type_id,
            position=position,
        )

        self._index += 1
        self._entity_by_id[entity.id] = entity

        self.entities.append(entity)

        return entity.id

    def update(self, entity_id: int, action: Action, value: float) -> None:
        entity = self._entity_by_id[entity_id]

        if action == Action.IDLE:
            pass
        if action == Action.MOVE:
            entity.direction = Direction(int(value))

        entity.action = action

    def remove(self, entity_id: int) -> None:
        self.entities.remove(self._entity_by_id[entity_id])
        del self._entity_by_id[entity_id]

    def prepare_for_entity_id(self, entity_id: int) -> CommonScene:
        this_entity = self._entity_by_id[entity_id]

        entities = []
        distance_x = math.ceil(TILES_X / 2)
        distance_y = math.ceil(TILES_Y / 2)

        # XXX Too expensive, preserve spatial matrix
        for that_entity in self.entities:
            if abs(this_entity.position.x - that_entity.position.x) > distance_x:
                continue
            if abs(this_entity.position.y - that_entity.position.y) > distance_y:
                continue

            entities.append(that_entity)

        return CommonScene(
            width=TILES_X,
            height=TILES_Y,
            anchor=this_entity.position,
            entities=entities,
        )

    @classmethod
    def new_from_description(cls, description: Description) -> "Scene":
        scene = cls(width=description.width, height=description.height)

        for layer in description.layers:
            for index, type_id in enumerate(layer.entities):
                if type_id == EntityType.EMPTY:
                    continue

                position = Vector()
                position.x = index % scene.width
                position.y = int(index / scene.width)

                scene.add(type_id, position)

        return scene
