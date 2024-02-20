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

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.scanner import Description
from ...common.logger import logger
from ...common.utils import (
    get_project_path,
    valid_project,
)
from ...common.definitions import (
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
)


@Gtk.Template(resource_path="/dev/tchx84/gameeky/player/widgets/session_join_window.ui")  # fmt: skip
class SessionJoinWindow(Adw.Window):
    __gtype_name__ = "SessionJoinWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    project = Gtk.Template.Child()
    entity_type = Gtk.Template.Child()
    address = Gtk.Template.Child()
    session_port = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self.project.props.text = get_project_path("")
        self.address.props.text = DEFAULT_ADDRESS
        self.session_port.props.value = DEFAULT_SESSION_PORT

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

    @Gtk.Template.Callback("on_create_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        if not valid_project(self.project_path):
            self._notify("A valid project must be provided")
            return

        if not self.network_address:
            self._notify("A valid address must be provided")
            return

        self.emit("done")
        self.close()

    @property
    def project_path(self) -> str:
        return self.project.props.text

    @property
    def network_address(self) -> str:
        return self.address.props.text

    @property
    def description(self) -> Description:
        return Description(
            project_path=self.project_path,
            entity_type=int(self.entity_type.props.value),
            address=self.network_address,
            session_port=int(self.session_port.props.value),
        )
