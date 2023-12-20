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
    def model(self, model: Optional[SceneModel]) -> None:
        self._view.model = model
