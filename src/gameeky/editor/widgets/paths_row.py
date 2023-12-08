from typing import List

from gi.repository import Gtk, GObject

from .path_row import PathRow


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/paths_row.ui")
class PathsRow(Gtk.Box):
    __gtype_name__ = "PathsRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    button = Gtk.Template.Child()
    rows = Gtk.Template.Child()

    def _add(self, path: str) -> None:
        row = PathRow()
        row.path = path
        row.connect("changed", self.__on_changed)
        row.connect("removed", self.__on_removed)

        self.rows.append(row)
        self.emit("changed")

    def _remove(self, row: PathRow) -> None:
        row.disconnect_by_func(self.__on_changed)
        row.disconnect_by_func(self.__on_removed)

        self.rows.remove(row)
        self.emit("changed")

    def __on_changed(self, row: PathRow) -> None:
        self.emit("changed")

    def __on_removed(self, row: PathRow) -> None:
        self._remove(row)

    @Gtk.Template.Callback("on_button_clicked")
    def __on_button_clicked(self, button: Gtk.Button) -> None:
        self._add("")

    @property
    def paths(self) -> List[str]:
        return [row.path for row in list(self.rows)]

    @paths.setter
    def paths(self, paths: List[str]) -> None:
        for row in list(self.rows):
            self._remove(row)

        for path in paths:
            self._add(path)
