from gi.repository import Gtk

from ...client.game.scene import Scene as SceneModel
from ...client.graphics.scene import Scene as SceneGraphics

from ...common.definitions import TILES_X, TILES_Y


class Scene(Gtk.AspectFrame):
    def __init__(self, model: SceneModel) -> None:
        super().__init__()

        view = SceneGraphics(model=model)
        view.set_vexpand(True)
        view.set_hexpand(True)

        self.set_obey_child(False)
        self.set_ratio(TILES_X / TILES_Y)
        self.set_child(view)
