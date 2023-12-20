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

from typing import List

from gi.repository import Gtk, GObject

from .path_row import PathRow


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/paths_row.ui")
class PathsRow(Gtk.Box):
    __gtype_name__ = "PathsRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    button = Gtk.Template.Child()
    rows = Gtk.Template.Child()

    def _add(self, path: str) -> None:
        row = PathRow()
        row.path = path
        row.connect("changed", self.__on_changed)
        row.connect("removed", self.__on_removed)

        self.rows.append(row)
        self.emit("changed")

    def _remove(self, row: PathRow) -> None:
        row.disconnect_by_func(self.__on_changed)
        row.disconnect_by_func(self.__on_removed)

        self.rows.remove(row)
        self.emit("changed")

    def __on_changed(self, row: PathRow) -> None:
        self.emit("changed")

    def __on_removed(self, row: PathRow) -> None:
        self._remove(row)

    @Gtk.Template.Callback("on_button_clicked")
    def __on_button_clicked(self, button: Gtk.Button) -> None:
        self._add("")

    @property
    def paths(self) -> List[str]:
        return [row.path for row in list(self.rows)]

    @paths.setter
    def paths(self, paths: List[str]) -> None:
        for row in list(self.rows):
            self._remove(row)

        for path in paths:
            self._add(path)
