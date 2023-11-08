import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import List

from gi.repository import Gtk, GObject

from .actuator_row import ActuatorRow


@Gtk.Template(filename=os.path.join(__dir__, "actuators_row.ui"))
class ActuatorsRow(Gtk.Box):
    __gtype_name__ = "ActuatorsRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    actuators = Gtk.Template.Child()

    def _add(self, name: str) -> None:
        row = ActuatorRow()
        row.value = name
        row.connect("changed", self.__on_changed)
        row.connect("removed", self.__on_removed)

        self.actuators.append(row)

    def _remove(self, row):
        row.disconnect_by_func(self.__on_changed)
        row.disconnect_by_func(self.__on_removed)

        self.actuators.remove(row)

    @Gtk.Template.Callback("on_clicked")
    def __on_clicked(self, button: Gtk.Button) -> None:
        self._add("")
        self.emit("changed")

    def __on_changed(self, row: ActuatorRow) -> None:
        self.emit("changed")

    def __on_removed(self, row: ActuatorRow) -> None:
        self._remove(row)
        self.emit("changed")

    @property
    def value(self) -> List[str]:
        return [actuator.value for actuator in list(self.actuators)]

    @value.setter
    def value(self, values: List[str]) -> None:
        for actuator in list(self.actuators):
            self.actuators.append(actuator)

        for value in values:
            self._add(value)
