from gi.repository import GLib

from .entity import EntityRegistry

from ..game.scene import Scene as SceneModel


class Scene:
    def __init__(self, model: SceneModel) -> None:
        self._handler_id = None

        self._model = model
        self._model.connect("ticked", self.__on_scene_updated)
        self._model.connect("updated", self.__on_scene_updated)

    def __on_scene_updated(self, model: SceneModel) -> None:
        if self._handler_id is None:
            self._handler_id = GLib.idle_add(self._play)

    def _play(self) -> int:
        for entity in self._model.entities:
            EntityRegistry.play(entity)

        self._handler_id = None
        return GLib.SOURCE_REMOVE
