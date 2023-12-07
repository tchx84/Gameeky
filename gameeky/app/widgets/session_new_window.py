import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.scanner import Description
from ...common.logger import logger
from ...common.utils import (
    get_data_path,
    get_data_folder,
    valid_project,
    valid_file,
)
from ...common.definitions import (
    Format,
    DEFAULT_ADDRESS,
    DEFAULT_SCENE,
    DEFAULT_CLIENTS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
    DEFAULT_STATS_PORT,
)


@Gtk.Template(filename=os.path.join(__dir__, "session_new_window.ui"))
class SessionNewWindow(Adw.Window):
    __gtype_name__ = "SessionNewWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    project = Gtk.Template.Child()
    scene = Gtk.Template.Child()
    players = Gtk.Template.Child()
    session_port = Gtk.Template.Child()
    messages_port = Gtk.Template.Child()
    scene_port = Gtk.Template.Child()
    stats_port = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self.project.props.text = get_data_path("")
        self.scene.props.text = DEFAULT_SCENE
        self.players.props.value = DEFAULT_CLIENTS
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
        folder = get_data_folder("")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
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

    @Gtk.Template.Callback("on_scene_clicked")
    def __on_scene_clicked(self, button: Gtk.Button) -> None:
        folder = get_data_folder(os.path.join(self.project_path, "scenes"))

        json_filter = Gtk.FileFilter()
        json_filter.add_pattern(f"*.{Format.SCENE}")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.default_filter = json_filter
        dialog.open(callback=self.__on_scene_finish)

    def __on_scene_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.scene.props.text = file.get_path()

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_create_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        if not valid_project(self.project_path):
            self._notify("A valid project must be provided")
            return

        if not valid_file(self.scene_path):
            self._notify("A valid scene must be provided")
            return

        self.emit("done")
        self.close()

    @property
    def project_path(self) -> str:
        return self.project.props.text

    @property
    def scene_path(self) -> str:
        return os.path.join(self.project_path, self.scene.props.text)

    @property
    def description(self) -> Description:
        return Description(
            address=DEFAULT_ADDRESS,
            data_path=self.project_path,
            scene_path=self.scene_path,
            clients=int(self.players.props.value),
            session_port=int(self.session_port.props.value),
            messages_port=int(self.messages_port.props.value),
            scene_port=int(self.scene_port.props.value),
            stats_port=int(self.stats_port.props.value),
        )
