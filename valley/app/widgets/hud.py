from gi.repository import Gtk

from ...client.game.stats import Stats as StatsModel
from ...client.graphics.hud import Hud as HudGraphics

from ...common.definitions import TILES_X, TILES_Y


class Hud(Gtk.AspectFrame):
    def __init__(self, model: StatsModel) -> None:
        super().__init__()

        view = HudGraphics(model=model)
        view.set_vexpand(True)
        view.set_hexpand(True)

        self.set_obey_child(False)
        self.set_ratio(TILES_X / TILES_Y)
        self.set_child(view)
