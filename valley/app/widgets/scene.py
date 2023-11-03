from typing import Optional
from gi.repository import Gtk

from ...client.game.scene import Scene as SceneModel
from ...client.graphics.scene import Scene as SceneGraphics

from ...common.definitions import TILES_X, TILES_Y


class Scene(Gtk.AspectFrame):
    def __init__(self) -> None:
        super().__init__()

        self._view = SceneGraphics()
        self._view.set_vexpand(True)
        self._view.set_hexpand(True)

        self.set_obey_child(False)
        self.set_ratio(TILES_X / TILES_Y)
        self.set_child(self._view)

    @property
    def model(self) -> Optional[SceneModel]:
        return self._view.model

    @model.setter
    def model(self, model: SceneModel) -> None:
        self._view.model = model
