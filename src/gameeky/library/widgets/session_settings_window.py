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

from gi.repository import Gio, Gtk, Adw

from ..utils import (
    get_session_project,
    get_session_entity_type,
    get_session_address,
    get_session_port,
    set_session_project,
    set_session_entity_type,
    set_session_address,
    set_session_port,
)

from ...common.logger import logger
from ...common.utils import valid_project


@Gtk.Template(resource_path="/dev/tchx84/gameeky/library/widgets/session_settings_window.ui")  # fmt: skip
class SessionSettingsWindow(Adw.Window):
    __gtype_name__ = "SessionSettingsWindow"

    toast = Gtk.Template.Child()
    project = Gtk.Template.Child()
    entity_type = Gtk.Template.Child()
    address = Gtk.Template.Child()
    session_port = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self.project.props.text = get_session_project()
        self.address.props.text = get_session_address()
        self.entity_type.props.value = get_session_entity_type()
        self.session_port.props.value = get_session_port()

    def _notify(self, title) -> None:
        toast = Adw.Toast()
        toast.props.title = title
        toast.props.timeout = 3

        self.toast.add_toast(toast)

    @Gtk.Template.Callback("on_project_clicked")
    def __on_project_clicked(self, button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog()
        dialog.select_folder(callback=self.on_project_finished)

    def on_project_finished(
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

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_save_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        if not valid_project(self.project.props.text):
            self._notify("A valid project must be provided")
            return

        if not self.address.props.text:
            self._notify("A valid address must be provided")
            return

        set_session_project(self.project.props.text)
        set_session_entity_type(int(self.entity_type.props.value))
        set_session_address(self.address.props.text)
        set_session_port(int(self.session_port.props.value))

        self.close()
