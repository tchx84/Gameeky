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
from gi.repository import Gtk, GLib, Graphene

from .status import Status
from .entity import EntityRegistry

from ..game.stats import Stats as StatsModel

from ...common import colors
from ...common.definitions import EntityType, TILES_X, TILES_Y, TICK


class Hud(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._model: Optional[StatsModel] = None

        GLib.timeout_add(TICK, self.__on_tick)

    def __on_tick(self) -> int:
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def _do_snapshot_entity(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / TILES_X
        tile_height = screen_height / TILES_Y

        rect = Graphene.Rect()
        rect.init(0, 0, tile_width / 2, tile_height / 2)

        snapshot.append_color(colors.BLACK, rect)

        rect = Graphene.Rect()
        rect.init(0, 0, tile_width / 2, tile_height / 2)

        snapshot.append_color(colors.BLACK, rect)

        if self._model.held == EntityType.EMPTY:
            return

        _, _, texture = EntityRegistry.get_default_texture(self._model.held)

        snapshot.append_texture(texture, rect)

    def _do_snapshot_status(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / TILES_X
        tile_height = screen_height / TILES_Y

        Status.draw(
            snapshot,
            self._model.durability,
            tile_width / 2,
            0,
            tile_width * 3,
            tile_height / 4,
        )

        Status.draw(
            snapshot,
            self._model.stamina,
            tile_width / 2,
            tile_height / 4,
            tile_width * 3,
            tile_height / 4,
            colors.BLUE,
        )

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / TILES_X
        tile_height = screen_height / TILES_Y

        anchor = Graphene.Point()
        anchor.init(
            x=(screen_width / 2) - (tile_width * 1.75),
            y=screen_height - tile_height,
        )

        snapshot.translate(anchor)

        self._do_snapshot_entity(snapshot)
        self._do_snapshot_status(snapshot)

    @property
    def model(self) -> Optional[StatsModel]:
        return self._model

    @model.setter
    def model(self, model: Optional[StatsModel]) -> None:
        self._model = model
        self.queue_draw()
