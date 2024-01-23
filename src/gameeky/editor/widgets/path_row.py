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

from gi.repository import Gio, Gtk, GObject

from .change_signal_helper import ChangeSignalHelper

from ...common.utils import get_project_folder, get_relative_path
from ...common.logger import logger


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/path_row.ui")
class PathRow(Gtk.Box):
    __gtype_name__ = "PathRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    entry = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._changes = ChangeSignalHelper(self.__on_changed)
        self._changes.add(self.entry)

    def __on_changed(self, entry: Gtk.Entry) -> None:
        self.emit("changed")

    @Gtk.Template.Callback("on_remove_button_clicked")
    def __on_remove_button_clicked(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @Gtk.Template.Callback("on_open_button_clicked")
    def __on_open_button_clicked(self, button: Gtk.Button) -> None:
        folder = get_project_folder("assets")

        ogg_filter = Gtk.FileFilter()
        ogg_filter.add_pattern("*.ogg")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.default_filter = ogg_filter
        dialog.open(callback=self.__on_open_dialog_finish)

    def __on_open_dialog_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.entry.props.text = get_relative_path(file.get_path())

    @property
    def path(self) -> str:
        return self.entry.props.text

    @path.setter
    def path(self, path: str) -> None:
        self._changes.block()

        self.entry.props.text = get_relative_path(path)

        self._changes.unblock()
