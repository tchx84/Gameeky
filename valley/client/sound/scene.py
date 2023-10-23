from .entity import EntityRegistry

from ..game.scene import Scene as SceneModel


class Scene:
    def __init__(self, model: SceneModel) -> None:
        self._model = model
        self._model.connect("updated", self.__on_scene_updated)

    def __on_scene_updated(self, model: SceneModel) -> None:
        for entity in self._model.entities:
            EntityRegistry.play(entity)
