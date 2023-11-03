import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from .scene import Scene as SceneWidget
from .hud import Hud as HudWidget

from ...client.game.scene import Scene as SceneModel
from ...client.game.stats import Stats as StatsModel


@Gtk.Template(filename=os.path.join(__dir__, "window.ui"))
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    stack = Gtk.Template.Child()
    overlay = Gtk.Template.Child()

    def switch_to_loading(self) -> None:
        self.stack.set_visible_child_name("loading")

    def switch_to_game(
        self,
        scene: SceneModel,
        stats: StatsModel,
    ) -> None:
        scene = SceneWidget(model=scene)
        hud = HudWidget(model=stats)

        self.overlay.add_overlay(scene)
        self.overlay.add_overlay(hud)

        self.stack.set_visible_child_name("game")
