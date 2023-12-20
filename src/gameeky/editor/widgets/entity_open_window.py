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

import os

from typing import Optional

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.logger import logger
from ...common.scanner import Description
from ...common.definitions import Format
from ...common.utils import (
    get_project_path,
    get_project_folder,
    valid_file,
    valid_project,
)


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/entity_open_window.ui")  # fmt: skip
class EntityOpenWindow(Adw.Window):
    __gtype_name__ = "EntityOpenWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    project = Gtk.Template.Child()
    entity = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._description: Optional[Description] = None
        self.project.props.text = get_project_path("")

    def _notify(self, title) -> None:
        toast = Adw.Toast()
        toast.props.title = title
        toast.props.timeout = 3

        self.toast.add_toast(toast)

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_open_clicked")
    def __on_open_clicked(self, button: Gtk.Button) -> None:
        if not valid_project(self.project_path):
            self._notify("A valid project must be provided")
            return

        if not valid_file(self.entity_path):
            self._notify("A valid entity must be provided")
            return

        self.emit("done")
        self.close()

    @Gtk.Template.Callback("on_path_open_clicked")
    def __on_path_open_clicked(self, button: Gtk.Button) -> None:
        folder = get_project_folder("")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.select_folder(callback=self.__on_path_open_finish)

    def __on_path_open_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.select_folder_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.project.props.text = file.get_path()

    @Gtk.Template.Callback("on_entity_open_clicked")
    def __on_entity_open_clicked(self, button: Gtk.Button) -> None:
        folder = get_project_folder(os.path.join(self.project_path, "entities"))

        json_filter = Gtk.FileFilter()
        json_filter.add_pattern(f"*.{Format.ENTITY}")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.default_filter = json_filter
        dialog.open(callback=self.__on_entity_open_finish)

    def __on_entity_open_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            path = file.get_path()
            self.entity.props.text = path
            self._description = Description.new_from_json(path)

    @property
    def entity_path(self) -> str:
        return self.entity.props.text

    @property
    def project_path(self) -> str:
        return self.project.props.text

    @property
    def description(self) -> Optional[Description]:
        return self._description
