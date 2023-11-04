from typing import Optional
from gi.repository import GLib

from .entity import EntityRegistry

from ..game.scene import Scene as SceneModel


class Scene:
    def __init__(self) -> None:
        self._handler_id: Optional[int] = None
        self._model: Optional[SceneModel] = None

    def __on_model_updated(self, model: SceneModel) -> None:
        if self._handler_id is None:
            self._handler_id = GLib.idle_add(self._play)

    def _reset_play(self) -> int:
        GLib.Source.remove(self._handler_id)
        self._handler_id = None
        return GLib.SOURCE_REMOVE

    def _play(self) -> int:
        if self._model is not None:
            for entity in self._model.entities:
                EntityRegistry.play(entity)

        return self._reset_play()

    def shutdown(self) -> None:
        if self._handler_id is not None:
            self._reset_play()
        if self._model is not None:
            self._model.disconnect_by_func(self.__on_model_updated)

        self._model = None
        self._handler_id = None

    @property
    def model(self) -> Optional[SceneModel]:
        return self._model

    @model.setter
    def model(self, model: Optional[SceneModel]) -> None:
        self.shutdown()

        self._model = model

        if self._model is not None:
            self._model.connect("ticked", self.__on_model_updated)
