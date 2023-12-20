# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
    def model(self) -> Optional[StatsModel]:
        return self._view.model

    @model.setter
    def model(self, model: Optional[StatsModel]) -> None:
        self._view.model = model
