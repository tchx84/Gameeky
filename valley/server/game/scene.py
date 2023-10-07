from typing import Dict

from gi.repository import GLib, GObject

from .entity import Entity

from ...common.action import Action
from ...common.definitions import TICK
from ...common.scene import Scene as CommonScene


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, width: int, height: int) -> None:
        CommonScene.__init__(self, width, height)
        GObject.GObject.__init__(self)

        self._entities = 0
        self._entity_by_id: Dict[int, Entity] = {}

        GLib.timeout_add(TICK, self.__on_scene_ticked)

    def __on_scene_ticked(self) -> None:
        for entity in self._entity_by_id.values():
            if entity.action == Action.MOVE:
                entity.move()

        self.emit("ticked")

        return GLib.SOURCE_CONTINUE

    def add(self) -> int:
        entity = Entity(id=self._entities)

        self._entities += 1
        self._entity_by_id[entity.id] = entity

        self.entities.append(entity)

        return entity.id

    def update(self, entity_id: int, action: Action, value: float) -> None:
        entity = self._entity_by_id[entity_id]
        entity.action = action
        entity.angle = value

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
