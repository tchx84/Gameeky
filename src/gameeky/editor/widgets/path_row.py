from gi.repository import Gio, Gtk, GObject

from ...common.utils import get_data_folder, get_relative_path
from ...common.logger import logger


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/path_row.ui")
class PathRow(Gtk.Box):
    __gtype_name__ = "PathRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    entry = Gtk.Template.Child()

    @Gtk.Template.Callback("on_changed")
    def __on_changed(self, entry: Gtk.Entry) -> None:
        self.emit("changed")

    @Gtk.Template.Callback("on_remove_button_clicked")
    def __on_remove_button_clicked(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @Gtk.Template.Callback("on_open_button_clicked")
    def __on_open_button_clicked(self, button: Gtk.Button) -> None:
        folder = get_data_folder("assets")

        ogg_filter = Gtk.FileFilter()
        ogg_filter.add_pattern("*.ogg")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.default_filter = ogg_filter
        dialog.open(callback=self.__on_open_dialog_finish)

    def __on_open_dialog_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.path = file.get_path()

    @property
    def path(self) -> str:
        return self.entry.props.text

    @path.setter
    def path(self, path: str) -> None:
        self.entry.props.text = get_relative_path(path)
