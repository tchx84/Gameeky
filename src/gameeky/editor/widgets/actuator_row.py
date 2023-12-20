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

from gi.repository import Gtk, Adw, GObject

from .dropdown_helper import DropDownHelper

from ..models.actuator_row import ActuatorRow as ActuatorRowModel


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/actuator_row.ui")
class ActuatorRow(Adw.ActionRow):
    __gtype_name__ = "ActuatorRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "moved": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    dropdown = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._dropdown = DropDownHelper(self.dropdown, ActuatorRowModel)
        self._dropdown.connect("changed", self.__on_changed)

    def __on_changed(self, dropdown: DropDownHelper) -> None:
        self.emit("changed")

    @Gtk.Template.Callback("on_moved")
    def __on_moved(self, button: Gtk.Button) -> None:
        self.emit("moved")

    @Gtk.Template.Callback("on_removed")
    def __on_removed(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @property
    def value(self) -> str:
        return self._dropdown.value

    @value.setter
    def value(self, value: str) -> None:
        self._dropdown.value = value
