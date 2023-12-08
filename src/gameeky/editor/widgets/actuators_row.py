from typing import List

from gi.repository import Gtk, GObject

from .actuator_row import ActuatorRow


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/actuators_row.ui")
class ActuatorsRow(Gtk.Box):
    __gtype_name__ = "ActuatorsRow"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    actuators = Gtk.Template.Child()

    def _add(self, value: str) -> None:
        row = ActuatorRow()
        row.value = value
        row.connect("changed", self.__on_changed)
        row.connect("removed", self.__on_removed)
        row.connect("moved", self.__on_moved)

        self.actuators.append(row)

    def _remove(self, row):
        row.disconnect_by_func(self.__on_changed)
        row.disconnect_by_func(self.__on_removed)
        row.disconnect_by_func(self.__on_moved)

        self.actuators.remove(row)

    def _move(self, row):
        actuators = list(self.actuators)
        index = actuators.index(row)

        if index == 0:
            sibbling = actuators[-1]
        elif index == 1:
            sibbling = None
        else:
            sibbling = actuators[index - 2]

        self.actuators.reorder_child_after(row, sibbling)

    @Gtk.Template.Callback("on_clicked")
    def __on_clicked(self, button: Gtk.Button) -> None:
        self._add("")
        self.emit("changed")

    def __on_changed(self, row: ActuatorRow) -> None:
        self.emit("changed")

    def __on_removed(self, row: ActuatorRow) -> None:
        self._remove(row)
        self.emit("changed")

    def __on_moved(self, row: ActuatorRow) -> None:
        self._move(row)
        self.emit("changed")

    @property
    def value(self) -> List[str]:
        return [actuator.value for actuator in list(self.actuators)]

    @value.setter
    def value(self, values: List[str]) -> None:
        for actuator in list(self.actuators):
            self._remove(actuator)

        for value in values:
            self._add(value)
