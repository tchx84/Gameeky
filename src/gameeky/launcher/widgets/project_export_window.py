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

from gettext import gettext as _

from gi.repository import Gtk, Gio, Adw

from ..models.project import Exporter

from ...common.definitions import Format
from ...common.logger import logger


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/project_export_window.ui")  # fmt: skip
class ProjectExportWindow(Adw.Window):
    __gtype_name__ = "ProjectExportWindow"

    header = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    progress = Gtk.Template.Child()

    def __init__(self, source: str, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._source = source

    @Gtk.Template.Callback("on_begin_clicked")
    def __on_begin_clicked(self, button: Gtk.Button) -> None:
        default_filter = Gtk.FileFilter()
        default_filter.add_pattern(f"*.{Format.PROJECT}")

        dialog = Gtk.FileDialog()
        dialog.props.initial_name = _("untitled") + f".{Format.PROJECT}"
        dialog.props.default_filter = default_filter
        dialog.save(callback=self.__on_begin_finished)

    def __on_begin_finished(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.save_finish(result)
        except Exception as e:
            logger.error(e)
            return

        exporter = Exporter(self._source, file.get_path())
        exporter.connect("started", self.__on_exporter_started)
        exporter.connect("progressed", self.__on_exporter_progressed)
        exporter.connect("finished", self.__on_exporter_finished)
        exporter.connect("failed", self.__on_exporter_failed)
        exporter.start()

        self.header.props.sensitive = False

    def __on_exporter_started(self, exporter: Exporter) -> None:
        self.stack.props.visible_child_name = "progress"

    def __on_exporter_progressed(self, exporter: Exporter, progress: float) -> None:
        self.progress.props.fraction = progress

    def __on_exporter_finished(self, exporter: Exporter) -> None:
        self.stack.props.visible_child_name = "finished"
        self.header.props.sensitive = True

    def __on_exporter_failed(self, exporter: Exporter) -> None:
        self.stack.props.visible_child_name = "failed"
        self.header.props.sensitive = True
