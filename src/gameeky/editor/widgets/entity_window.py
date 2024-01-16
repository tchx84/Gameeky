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

from gi.repository import Gtk, GObject, Adw

from .global_settings import GlobalSettings
from .entity_settings import EntitySettings
from .animations_settings import AnimationsSettings
from .sounds_settings import SoundsSettings

from ...common.scanner import Description
from ...common.definitions import Format
from ...common.monitor import Monitor


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/entity_window.ui")  # fmt: skip
class EntityWindow(Adw.ApplicationWindow):
    __gtype_name__ = "EntityWindow"

    __gsignals__ = {
        "reload": (GObject.SignalFlags.RUN_LAST, None, ()),
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    game_box = Gtk.Template.Child()
    graphics_box = Gtk.Template.Child()
    sound_box = Gtk.Template.Child()
    banner = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._global_settings = GlobalSettings()
        self._entity_settings = EntitySettings()
        self._animations_settings = AnimationsSettings()
        self._sounds_settings = SoundsSettings()

        self.game_box.append(self._global_settings)
        self.game_box.append(self._entity_settings)
        self.graphics_box.append(self._animations_settings)
        self.sound_box.append(self._sounds_settings)

        self._global_settings.connect("changed", self.__on_changed)
        self._entity_settings.connect("changed", self.__on_changed)
        self._animations_settings.connect("changed", self.__on_changed)
        self._sounds_settings.connect("changed", self.__on_changed)

        Monitor.default().connect("changed", self.__on_monitor_changed)

    def __on_changed(self, *args) -> None:
        self.emit("changed")

    def __on_monitor_changed(self, monitor: Monitor) -> None:
        self.banner.props.revealed = True

    @Gtk.Template.Callback("on_reload_clicked")
    def __on_reload_clicked(self, *args) -> None:
        self.emit("reload")
        self.banner.props.revealed = False

    @property
    def suggested_name(self) -> str:
        prefix = f"{self._global_settings.description.id:04d}"
        suffix = f"{self._entity_settings.description.name.lower()}"

        return f"{prefix}_{suffix}.{Format.ENTITY}"

    @property
    def description(self) -> Description:
        description = self._global_settings.description
        description.game.default = self._entity_settings.description
        description.graphics = self._animations_settings.description
        description.sound = self._sounds_settings.description

        return description

    @description.setter
    def description(self, description: Description) -> None:
        self._global_settings.description = description
        self._entity_settings.description = description.game.default
        self._animations_settings.description = description.graphics
        self._sounds_settings.description = description.sound
