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

from typing import Tuple

from gi.repository import Gtk

from ...common.utils import clamp
from ...client.graphics.scene import Scene as SceneGraphics


class Scene(SceneGraphics):
    TILE_SIZE = 10

    def __init__(self) -> None:
        super().__init__(editing=True)
        self._scale = 1.0

        self.props.hexpand = True
        self.props.vexpand = True

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE

    def do_measure(
        self,
        orientation: Gtk.Orientation,
        for_size: int,
    ) -> Tuple[float, ...]:
        if self._model is None:
            return (0, 0, -1, -1)

        if orientation == Gtk.Orientation.HORIZONTAL:
            width = self._model.width * self.TILE_SIZE * self.scale
            return (width, width, -1, -1)
        else:
            height = self._model.height * self.TILE_SIZE * self.scale
            return (height, height, -1, -1)

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        self._scale = clamp(10.0, 1.0, scale)
        self.queue_resize()
