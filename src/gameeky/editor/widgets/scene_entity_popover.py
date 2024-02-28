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

from enum import StrEnum, auto

from typing import Optional
from gi.repository import Gdk, Gtk, GObject

from .entity_row import EntityRow

from ...common.utils import launch_entity, get_project_path


class Operation(StrEnum):
    EDIT = auto()
    DELETE = auto()
    ADD = auto()


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/scene_entity_popover.ui")  # fmt: skip
class SceneEntityPopover(Gtk.Popover):
    __gtype_name__ = "SceneEntityPopover"

    __gsignals__ = {
        "deleted": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    edit = Gtk.Template.Child()
    delete = Gtk.Template.Child()
    add = Gtk.Template.Child()

    def __init__(self, parent: Gtk.Widget) -> None:
        super().__init__()
        self._entity: Optional[EntityRow] = None
        self.set_parent(parent)

    def _update_buttons(self, entity: Optional[EntityRow]) -> None:
        sensitive = entity is not None

        self.edit.props.sensitive = sensitive
        self.delete.props.sensitive = sensitive

    def _emit_deleted(self) -> None:
        if self._entity is None:
            return

        self.emit("deleted", self._entity.model)

    @Gtk.Template.Callback("on_activated")
    def __on_activated(self, box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        operation = row.props.name

        if operation == Operation.ADD:
            launch_entity(get_project_path(), "")
        elif operation == Operation.EDIT and self._entity is not None:
            launch_entity(get_project_path(), self._entity.model.path)
        elif operation == Operation.DELETE:
            self._emit_deleted()

        self.popdown()

    def display(self, entity: Optional[EntityRow], x: float, y: float) -> None:
        self._update_buttons(entity)
        self._entity = entity

        self.set_pointing_to(Gdk.Rectangle(x, y, 1, 1))
        self.set_offset(x, y)
        self.popup()
