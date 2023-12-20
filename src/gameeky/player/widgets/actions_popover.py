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

from gi.repository import Gdk, Gtk, GObject

from ...common.definitions import Action


@Gtk.Template(resource_path="/dev/tchx84/gameeky/player/widgets/actions_popover.ui")  # fmt: skip
class ActionsPopover(Gtk.Popover):
    __gtype_name__ = "ActionsPopover"

    __gsignals__ = {
        "performed": (GObject.SignalFlags.RUN_LAST, None, (int,)),
    }

    def __init__(self, parent: Gtk.Widget) -> None:
        super().__init__()
        self.set_parent(parent)

    @Gtk.Template.Callback("on_activated")
    def __on_activated(self, box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        self.emit("performed", Action[row.props.name.upper()])
        self.popdown()

    def display(self, x: int, y: int) -> None:
        self.set_pointing_to(Gdk.Rectangle(x, y, 0, 0))
        self.set_offset(x, y)
        self.popup()
