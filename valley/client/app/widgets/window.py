from gi.repository import Gtk

from .scene import Scene as SceneWidget
from .stats import Stats as StatsWidget

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
        stats = StatsWidget(model=stats_model)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.append(scene)
        box.append(stats)

        self.set_title("Valley")
        self.set_child(box)
