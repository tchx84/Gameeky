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

from .paths_row import PathsRow
from .sound_player import SoundPlayer

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/sound_settings.ui")  # fmt: skip
class SoundSettings(Adw.PreferencesGroup):
    __gtype_name__ = "SoundSettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    preview = Gtk.Template.Child()
    delay = Gtk.Template.Child()
    timeout = Gtk.Template.Child()
    paths = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._paths = PathsRow()
        self._paths.connect("changed", self.__on_changed)
        self.paths.append(self._paths)

        self._preview = SoundPlayer()
        self.preview.append(self._preview)

    @Gtk.Template.Callback("on_changed")
    def __on_changed(self, *args) -> None:
        self._preview.update(self.description)
        self.emit("changed")

    @property
    def description(self) -> Description:
        return Description(
            delay=round(self.delay.props.value, 1),
            timeout=round(self.timeout.props.value, 1),
            paths=self._paths.paths,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.delay.props.value = description.delay
        self.timeout.props.value = description.timeout
        self._paths.paths = description.paths

    def shutdown(self) -> None:
        self._preview.shutdown()
