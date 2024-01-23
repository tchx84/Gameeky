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

from gettext import gettext as _
from gi.repository import Gtk, Adw, GObject

from .sound_settings import SoundSettings
from .dropdown_helper import DropDownHelper
from .change_signal_helper import ChangeSignalHelper

from ..models.state_row import StateRow as StateRowModel

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/sound_row.ui")
class SoundRow(Adw.PreferencesGroup):
    __gtype_name__ = "SoundRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "cloned": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    state_combo = Gtk.Template.Child()
    sound_box = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._sound_settings = SoundSettings()
        self.sound_box.append(self._sound_settings)

        self._state = DropDownHelper(self.state_combo, StateRowModel)

        self._update_description()

        self._changes = ChangeSignalHelper(self.__on_changed)
        self._changes.add(self._state)
        self._changes.add(self._sound_settings)

    def __on_changed(self, *args) -> None:
        self._update_description()
        self.emit("changed")

    def _update_description(self) -> None:
        self.props.description = _("While %s") % self._state.text.lower()

    @Gtk.Template.Callback("on_remove_clicked")
    def __on_remove_clicked(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @Gtk.Template.Callback("on_clone_clicked")
    def __on_clone_clicked(self, button: Gtk.Button) -> None:
        self.emit("cloned")

    @property
    def state(self) -> str:
        return self._state.value

    @state.setter
    def state(self, value: str) -> None:
        self._changes.block()

        self._state.value = value
        self._update_description()

        self._changes.unblock()

    @property
    def description(self) -> Description:
        return self._sound_settings.description

    @description.setter
    def description(self, description: Description) -> None:
        self._changes.block()

        self._sound_settings.description = description

        self._changes.unblock()

    def shutdown(self) -> None:
        self._sound_settings.shutdown()
