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

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/global_settings.ui")  # fmt: skip
class GlobalSettings(Adw.PreferencesGroup):
    __gtype_name__ = "GlobalSettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    identifier = Gtk.Template.Child()

    @Gtk.Template.Callback("on_changed")
    def __on_changed(self, *args) -> None:
        self.emit("changed")

    @property
    def description(self) -> Description:
        return Description(
            id=int(self.identifier.props.value),
            game=Description(
                default=None,
            ),
            graphics=None,
            sound=None,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.identifier.props.value = description.id
