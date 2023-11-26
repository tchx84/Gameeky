import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw, GObject

from .utils import get_position_in_model

from ...server.game.actuators.base import ActuatorRegistry


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

        for name in ActuatorRegistry.names():
            self.model.append(name)

        # XXX Move to UI file
        self.dropdown.connect("notify::selected", self.__on_changed)

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
        position = get_position_in_model(self.model, value)

        if position is None:
            return

        self.dropdown.props.selected = position
