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

from .project_settings import ProjectSettings

from ..models.project import Project

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/project_edit_window.ui")  # fmt: skip
class ProjectEditWindow(Adw.Window):
    __gtype_name__ = "ProjectEditWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    content = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._project_settings = ProjectSettings()
        self.content.props.child = self._project_settings

    def _notify(self, title) -> None:
        toast = Adw.Toast()
        toast.props.title = title
        toast.props.timeout = 3

        self.toast.add_toast(toast)

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_save_clicked")
    def __on_save_clicked(self, button: Gtk.Button) -> None:
        description = self.description

        if not Project.sanitize(description.name):
            self._notify("A valid name must be provided")
            return

        if not description.description:
            self._notify("A valid description must be provided")
            return

        self.emit("done")
        self.close()

    @property
    def description(self) -> Description:
        return self._project_settings.description

    @description.setter
    def description(self, description: Description) -> None:
        self._project_settings.description = description
