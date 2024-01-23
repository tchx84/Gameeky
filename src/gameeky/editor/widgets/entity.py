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

from gi.repository import Gsk, Gdk, Gtk, Graphene

from ...client.graphics.entity import EntityRegistry


class Entity(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._type_id: Optional[int] = None

        self.visible = False
        self.props.hexpand = True
        self.props.vexpand = True

    def do_snapshot_entity(
        self,
        snapshot: Gtk.Snapshot,
        scale_x: float,
        scale_y: float,
        texture: Gdk.Texture,
    ) -> None:
        if texture is None:
            return

        ratio_x = 1.0 if scale_x >= scale_y else scale_x / scale_y
        ratio_y = 1.0 if scale_y >= scale_y else scale_y / scale_x

        rect_width = self.get_width() * ratio_x
        rect_height = self.get_height() * ratio_y

        rect_x = (self.get_width() / 2) - (rect_width / 2)
        rect_y = (self.get_height() / 2) - (rect_height / 2)

        rect = Graphene.Rect()
        rect.init(rect_x, rect_y, rect_width, rect_height)

        snapshot.append_scaled_texture(texture, Gsk.ScalingFilter.TRILINEAR, rect)

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._type_id is None:
            return

        scale_x, scale_y, texture = EntityRegistry.get_default_texture(self._type_id)
        self.do_snapshot_entity(snapshot, scale_x, scale_y, texture)

    @property
    def type_id(self) -> Optional[int]:
        return self._type_id

    @type_id.setter
    def type_id(self, type_id) -> None:
        self._type_id = type_id
        self.queue_draw()
