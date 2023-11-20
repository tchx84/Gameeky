import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.scanner import Description
from ...common.logger import logger
from ...common.utils import (
    get_data_path,
    valid_directory,
)
from ...common.definitions import (
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
    DEFAULT_STATS_PORT,
)


@Gtk.Template(filename=os.path.join(__dir__, "session_join_window.ui"))
class SessionJoinWindow(Adw.Window):
    __gtype_name__ = "SessionJoinWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    project = Gtk.Template.Child()
    address = Gtk.Template.Child()
    session_port = Gtk.Template.Child()
    messages_port = Gtk.Template.Child()
    scene_port = Gtk.Template.Child()
    stats_port = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self.project.props.text = get_data_path("")
        self.address.props.text = DEFAULT_ADDRESS
        self.session_port.props.value = DEFAULT_SESSION_PORT
        self.messages_port.props.value = DEFAULT_MESSAGES_PORT
        self.scene_port.props.value = DEFAULT_SCENE_PORT
        self.stats_port.props.value = DEFAULT_STATS_PORT

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
        if not valid_directory(self.project_path):
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
            data_path=self.project_path,
            address=self.network_address,
            session_port=int(self.session_port.props.value),
            messages_port=int(self.messages_port.props.value),
            scene_port=int(self.scene_port.props.value),
            stats_port=int(self.stats_port.props.value),
        )
