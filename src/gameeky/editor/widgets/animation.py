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

from gi.repository import Gtk, GLib

from .entity import Entity

from ...common.scanner import Description
from ...common.definitions import TICK

from ...client.graphics.entity import Animation as AnimationGraphics, EntityRegistry


class AnimationRenderer(Entity):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._animation: Optional[AnimationGraphics] = None
        self._handler_id = GLib.timeout_add(TICK, self.__on_entity_ticked)

    def __on_entity_ticked(self) -> int:
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._animation is None:
            return

        scale_x, scale_y, texture = self._animation.get_frame()
        self.do_snapshot_entity(snapshot, scale_x, scale_y, texture)

    def update(self, description: Description) -> None:
        self._animation = EntityRegistry.create_animation_from_description(description)

    def shutdown(self) -> None:
        GLib.Source.remove(self._handler_id)


class Animation(Gtk.AspectFrame):
    def __init__(self) -> None:
        super().__init__()

        self._renderer = AnimationRenderer()

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_obey_child(False)
        self.set_ratio(1)
        self.set_child(self._renderer)

    def update(self, description: Description) -> None:
        return self._renderer.update(description)

    def shutdown(self) -> None:
        self._renderer.shutdown()
