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

from pathlib import Path

from gi.repository import Gtk, Gio, GLib, Adw

from ..models.project import Importer

from ...common.definitions import Format
from ...common.logger import logger
from ...common.utils import get_projects_path, find_new_name


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/project_import_window.ui")  # fmt: skip
class ProjectImportWindow(Adw.Window):
    __gtype_name__ = "ProjectImportWindow"

    header = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    progress = Gtk.Template.Child()

    @Gtk.Template.Callback("on_begin_clicked")
    def __on_begin_clicked(self, button: Gtk.Button) -> None:
        default_filter = Gtk.FileFilter()
        default_filter.add_pattern(f"*.{Format.PROJECT}")

        dialog = Gtk.FileDialog()
        dialog.props.default_filter = default_filter
        dialog.open(callback=self.__on_begin_finished)

    def __on_begin_finished(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
            return

        projects_path = get_projects_path()
        project_name = find_new_name(projects_path, Path(file.get_path()).stem)
        target = GLib.build_filenamev([projects_path, project_name])

        importer = Importer(file.get_path(), target)
        importer.connect("started", self.__on_importer_started)
        importer.connect("progressed", self.__on_importer_progressed)
        importer.connect("finished", self.__on_importer_finished)
        importer.connect("failed", self.__on_importer_failed)
        importer.start()

        self.header.props.sensitive = False

    def __on_importer_started(self, importer: Importer) -> None:
        self.stack.props.visible_child_name = "progress"

    def __on_importer_progressed(self, importer: Importer, progress: float) -> None:
        self.progress.props.fraction = progress

    def __on_importer_finished(self, importer: Importer) -> None:
        self.stack.props.visible_child_name = "finished"
        self.header.props.sensitive = True

    def __on_importer_failed(self, importer: Importer) -> None:
        self.stack.props.visible_child_name = "failed"
        self.header.props.sensitive = True
