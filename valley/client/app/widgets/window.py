from gi.repository import Gtk

from .scene import Scene as SceneView

from ...game.scene import Scene as SceneModel


class Window(Gtk.ApplicationWindow):
    def __init__(self, application: Gtk.Application, model: SceneModel) -> None:
        super().__init__(application=application)

        scene = SceneView(model=model)

        self.set_title("Valley")
        self.set_child(scene)
