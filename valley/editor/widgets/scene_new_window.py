import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.logger import logger
from ...common.utils import get_data_path, get_data_folder, valid_directory
from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "scene_new_window.ui"))
class SceneNewWindow(Adw.Window):
    __gtype_name__ = "SceneNewWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    name = Gtk.Template.Child()
    project = Gtk.Template.Child()
    width = Gtk.Template.Child()
    height = Gtk.Template.Child()

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

    @Gtk.Template.Callback("on_create_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        if not self.title:
            self._notify("A valid name must be provided")
            return

        if not valid_directory(self.data_path):
            self._notify("A valid project must be provided")
            return

        self.emit("done")
        self.close()

    @Gtk.Template.Callback("on_open_clicked")
    def __on_open_clicked(self, button: Gtk.Button) -> None:
        folder = get_data_folder("")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.select_folder(callback=self.__on_open_dialog_finish)

    def __on_open_dialog_finish(
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

    @property
    def title(self) -> str:
        return self.name.props.text

    @property
    def data_path(self) -> None:
        return self.project.props.text

    @property
    def description(self) -> Description:
        return Description(
            name=self.name.props.text,
            width=int(self.width.props.value),
            height=int(self.height.props.value),
            spawn=Description(
                x=0,
                y=0,
                z=0,
            ),
            entities=[],
        )
