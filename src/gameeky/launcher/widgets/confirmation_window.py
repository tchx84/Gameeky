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

from gi.repository import Adw, Gtk, GObject


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/confirmation_window.ui")  # fmt: skip
class ConfirmationWindow(Adw.MessageDialog):
    __gtype_name__ = "ConfirmationWindow"

    __gsignals__ = {
        "confirmed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    @Gtk.Template.Callback("on_response_clicked")
    def __on_response_clicked(self, dialog, reponse: str) -> None:
        if reponse == "delete":
            self.emit("confirmed")
