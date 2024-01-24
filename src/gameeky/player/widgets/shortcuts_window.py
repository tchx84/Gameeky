# Copyright (c) 2024 Martín Abente Lahaye.
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

from gi.repository import Gtk


def present_shortcuts(window: Gtk.Window) -> None:
    builder = Gtk.Builder.new_from_resource("/dev/tchx84/gameeky/player/widgets/shortcuts_window.ui")  # fmt: skip
    dialog = builder.get_object("ShortcutsWindow")
    dialog.props.transient_for = window
    dialog.present()
