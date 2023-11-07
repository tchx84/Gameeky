import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import List

from gi.repository import Gtk, GObject

from .path import Path


@Gtk.Template(filename=os.path.join(__dir__, "paths.ui"))
class Paths(Gtk.Box):
    __gtype_name__ = "Paths"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    button = Gtk.Template.Child()
    entries = Gtk.Template.Child()

    def _add(self, path: str) -> None:
        entry = Path()
        entry.path = path
        entry.connect("changed", self.__on_changed)
        entry.connect("removed", self.__on_removed)

        self.entries.append(entry)

    def _remove(self, entry: Path) -> None:
        self.entries.remove(entry)

    def __on_changed(self, entry: Path) -> None:
        self.emit("changed")

    def __on_removed(self, entry: Path) -> None:
        self._remove(entry)
        self.emit("changed")

    @Gtk.Template.Callback("on_button_clicked")
    def __on_button_clicked(self, button: Gtk.Button) -> None:
        self._add("")

    @property
    def paths(self) -> List[str]:
        return [entry.path for entry in list(self.entries)]

    @paths.setter
    def paths(self, paths: List[str]) -> None:
        for entry in list(self.entries):
            self._remove(entry)

        for path in paths:
            self._add(path)
