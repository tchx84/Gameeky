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

from gi.repository import Gdk, Gtk, Graphene

from ...common import colors


class Status:
    @classmethod
    def draw(
        cls,
        snapshot: Gtk.Snapshot,
        value: float,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Optional[Gdk.RGBA] = None,
    ) -> None:
        # Stroke

        rect_x = x
        rect_y = y
        rect_width = width
        rect_height = height

        stroke = Graphene.Rect()
        stroke.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(colors.BLACK, stroke)

        # Background

        offset = rect_height * 0.25

        rect_x += offset
        rect_y += offset
        rect_width -= offset * 2
        rect_height -= offset * 2

        background = Graphene.Rect()
        background.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(colors.WHITE, background)

        ## Fill

        rect_width *= value

        fill = Graphene.Rect()
        fill.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(color if color is not None else colors.GREEN, fill)
