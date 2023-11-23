from typing import Optional
from gi.repository import Gtk

from ...client.game.stats import Stats as StatsModel
from ...client.graphics.hud import Hud as HudGraphics

from ...common.definitions import TILES_X, TILES_Y


class Hud(Gtk.AspectFrame):
    def __init__(self) -> None:
        super().__init__()

        self._view = HudGraphics()
        self._view.set_vexpand(True)
        self._view.set_hexpand(True)

        self.set_obey_child(False)
        self.set_ratio(TILES_X / TILES_Y)
        self.set_child(self._view)

    @property
    def canvas(self) -> Gtk.Widget:
        return self._view

    @property
    def model(self) -> Optional[StatsModel]:
        return self._view.model

    @model.setter
    def model(self, model: Optional[StatsModel]) -> None:
        self._view.model = model
