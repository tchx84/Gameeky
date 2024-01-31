# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Type, Optional, List

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
        exclude: Optional[List[str]] = None,
    ) -> None:
        super().__init__()

        self._model = cls.model(default=default, exclude=exclude)

        self._factory = Gtk.SignalListItemFactory()
        self._factory.connect("bind", self.__on_bind)
        self._factory.connect("setup", self.__on_setup)

        self._dropdown = dropdown
        self._dropdown.props.factory = self._factory
        self._dropdown.props.model = self._model
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
        self._dropdown.props.tooltip_text = self.tooltip
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
    def tooltip(self) -> str:
        return self._dropdown.props.selected_item.props.tooltip

    @property
    def text(self) -> str:
        return self._dropdown.props.selected_item.props.text

    @property
    def value(self) -> str:
        return self._dropdown.props.selected_item.props.value

    @value.setter
    def value(self, value: str) -> None:
        position = self.get_position_in_model(self._dropdown.props.model, value)

        if position is None:
            return

        self._dropdown.props.selected = position

    @property
    def index(self) -> int:
        return int(self._dropdown.props.selected)

    @index.setter
    def index(self, index: int) -> None:
        self._dropdown.props.selected = index
