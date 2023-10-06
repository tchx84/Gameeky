from gi.repository import GLib, GObject

from .entity import Entity

from ...common.action import Action
from ...common.scene import Scene as CommonScene


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    TICK = 100

    def __init__(self):
        CommonScene.__init__(self)
        GObject.GObject.__init__(self)

        self._entities = 0
        self._entity_by_id = {}
        self._actions_by_entity_id = {}

        GLib.timeout_add(self.TICK, self.__on_scene_ticked)

    def __on_scene_ticked(self):
        for entity_id, (action, value) in self._actions_by_entity_id.items():
            entity = self._entity_by_id.get(entity_id)

            if action == Action.MOVE:
                entity.angle = value
                entity.move()

        self._actions_by_entity_id = {}
        self.emit("ticked")

        return GLib.SOURCE_CONTINUE

    def add(self):
        entity = Entity(id=self._entities)

        self._entities += 1
        self._entity_by_id[entity.id] = entity

        self.entities.append(entity)

        return entity.id

    def qeueu(self, entity_id, action, value):
        self._actions_by_entity_id[entity_id] = (action, value)

    def remove(self, entity_id):
        self.entities.remove(self._entity_by_id.get(entity_id))

        if self._actions_by_entity_id.get(entity_id) is not None:
            del self._actions_by_entity_id[entity_id]

        del self._entity_by_id[entity_id]
