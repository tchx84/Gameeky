from typing import Type, Optional

from gi.repository import Gio, Gtk, GObject

from ..models.base_row import BaseRow as BaseRowModel


class DropDownHelper(GObject.GObject):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(
        self,
        dropdown: Gtk.DropDown,
        cls: Type[BaseRowModel],
        default=False,
    ) -> None:
        super().__init__()

        self._model = cls.model(default=default)

        self._factory = Gtk.SignalListItemFactory()
        self._factory.connect("bind", self.__on_bind)
        self._factory.connect("setup", self.__on_setup)

        self._dropdown = dropdown
        self._dropdown.props.model = self._model
        self._dropdown.props.factory = self._factory
        self._dropdown.connect("notify::selected", self.__on_changed)

    def __on_setup(
        self,
        factory: Gtk.SignalListItemFactory,
        item: Gtk.ListItem,
    ) -> None:
        child = Gtk.Label()
        child.props.xalign = 0

        item.set_child(child)

    def __on_bind(
        self,
        factory: Gtk.SignalListItemFactory,
        item: Gtk.ListItem,
    ) -> None:
        row = item.get_item()

        child = item.get_child()
        child.set_text(row.text)

    def __on_changed(self, entry: Gtk.DropDown, value: int) -> None:
        self.emit("changed")

    def get_position_in_model(self, model: Gio.ListStore, value: str) -> Optional[int]:
        for index, row in enumerate(list(model)):
            if row.props.value == value:
                return index

        return None

    @property
    def widget(self) -> Gtk.DropDown:
        return self._dropdown

    @property
    def value(self) -> str:
        return self._dropdown.props.selected_item.props.value

    @value.setter
    def value(self, value: str) -> None:
        position = self.get_position_in_model(self._dropdown.props.model, value)

        if position is None:
            return

        self._dropdown.props.selected = position
