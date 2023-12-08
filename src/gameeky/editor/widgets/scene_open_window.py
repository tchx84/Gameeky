import os

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.logger import logger
from ...common.utils import get_data_path, get_data_folder, valid_file, valid_project
from ...common.scanner import Description
from ...common.definitions import Format


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/scene_open_window.ui")  # fmt: skip
class SceneOpenWindow(Adw.Window):
    __gtype_name__ = "SceneOpenWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    project = Gtk.Template.Child()
    scene = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.project.props.text = get_data_path("")

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
        if not valid_project(self.data_path):
            self._notify("A valid project must be provided")
            return

        if not valid_file(self.scene_path):
            self._notify("A valid scene must be provided")
            return

        self.emit("done")
        self.close()

    @Gtk.Template.Callback("on_path_open_clicked")
    def __on_path_open_clicked(self, button: Gtk.Button) -> None:
        folder = get_data_folder("")

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

    @Gtk.Template.Callback("on_scene_open_clicked")
    def __on_scene_open_clicked(self, button: Gtk.Button) -> None:
        folder = get_data_folder(os.path.join(self.data_path, "scenes"))

        json_filter = Gtk.FileFilter()
        json_filter.add_pattern(f"*.{Format.SCENE}")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.default_filter = json_filter
        dialog.open(callback=self.__on_scene_open_finish)

    def __on_scene_open_finish(
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

    @property
    def scene_path(self) -> str:
        return os.path.join(self.data_path, self.scene.props.text)

    @property
    def data_path(self) -> str:
        return self.project.props.text

    @property
    def description(self) -> Description:
        return Description.new_from_json(self.scene_path)
