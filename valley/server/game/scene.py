from typing import Dict

from gi.repository import GLib, GObject

from .entity import Entity, EntityRegistry

from ...common.action import Action
from ...common.direction import Direction
from ...common.definitions import TICK
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
            if entity.action == Action.MOVE:
                entity.move()

    def add(self, type_id: int) -> int:
        entity = EntityRegistry.create_entity(id=self._index, type_id=type_id)

        self._index += 1
        self._entity_by_id[entity.id] = entity

        self.entities.append(entity)

        return entity.id

    def update(self, entity_id: int, action: Action, value: float) -> None:
        entity = self._entity_by_id[entity_id]

        if action == Action.NOTHING:
            pass
        if action == Action.MOVE:
            entity.direction = Direction(int(value))

        entity.action = action

    def remove(self, entity_id: int) -> None:
        self.entities.remove(self._entity_by_id[entity_id])
        del self._entity_by_id[entity_id]

    def prepare_for_entity_id(self, entity_id: int) -> CommonScene:
        entity = self._entity_by_id[entity_id]

        # XXX only include entities that the client can actually see
        return CommonScene(
            width=self.width,
            height=self.height,
            anchor=entity.position,
            entities=self.entities,
        )
