from gi.repository import Gtk

from .scene import Scene as SceneWidget
from .hud import Hud as HudWidget

from ...game.scene import Scene as SceneModel
from ...game.stats import Stats as StatsModel


class Window(Gtk.ApplicationWindow):
    def __init__(
        self,
        application: Gtk.Application,
        scene_model: SceneModel,
        stats_model: StatsModel,
    ) -> None:
        super().__init__(application=application)

        scene = SceneWidget(model=scene_model)
        hud = HudWidget(model=stats_model)

        box = Gtk.Overlay()
        box.add_overlay(scene)
        box.add_overlay(hud)

        self.set_title("Valley")
        self.set_child(box)
