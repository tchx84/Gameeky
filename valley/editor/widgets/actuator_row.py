import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import Optional

from gi.repository import Gtk, Adw, GObject


@Gtk.Template(filename=os.path.join(__dir__, "actuator_row.ui"))
class ActuatorRow(Adw.ActionRow):
    __gtype_name__ = "ActuatorRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    dropdown = Gtk.Template.Child()
    model = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()

        # XXX Move to UI file
        self.dropdown.connect("notify::selected", self.__on_changed)

    def _get_position(self, value: str) -> Optional[int]:
        for index, row in enumerate(list(self.model)):
            if row.props.string == value:
                return index

        return None

    def __on_changed(self, entry: Gtk.DropDown, value: int) -> None:
        self.emit("changed")

    @Gtk.Template.Callback("on_removed")
    def __on_removed(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @property
    def value(self) -> str:
        return self.dropdown.props.selected_item.props.string

    @value.setter
    def value(self, value: str) -> None:
        position = self._get_position(value)

        if position is None:
            return

        self.dropdown.props.selected = position
