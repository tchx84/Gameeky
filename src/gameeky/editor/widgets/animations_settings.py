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

from typing import Dict, Optional

from gi.repository import Gtk, GObject

from .animation_row import AnimationRow

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/animations_settings.ui")  # fmt: skip
class AnimationsSettings(Gtk.Box):
    __gtype_name__ = "AnimationsSettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    button = Gtk.Template.Child()
    animations_box = Gtk.Template.Child()

    def _add(
        self,
        state: Optional[str],
        direction: Optional[str],
        description: Optional[Description],
        prepend: bool = False,
    ) -> None:
        row = AnimationRow()
        row.connect("changed", self.__on_changed)
        row.connect("cloned", self.__on_cloned)
        row.connect("removed", self.__on_removed)

        if state is not None:
            row.state = state
        if direction is not None:
            row.direction = direction
        if description is not None:
            row.description = description

        if prepend is True:
            self.animations_box.prepend(row)
        else:
            self.animations_box.append(row)

        self.emit("changed")

    def _remove(self, row: AnimationRow) -> None:
        row.shutdown()
        row.disconnect_by_func(self.__on_changed)
        row.disconnect_by_func(self.__on_cloned)
        row.disconnect_by_func(self.__on_removed)

        self.animations_box.remove(row)

        self.emit("changed")

    def __on_changed(self, row: AnimationRow) -> None:
        self.emit("changed")

    def __on_removed(self, row: AnimationRow) -> None:
        self._remove(row)

    def __on_cloned(self, row: AnimationRow) -> None:
        self._add(row.state, row.direction, row.description, prepend=True)

    @Gtk.Template.Callback("on_clicked")
    def __on_clicked(self, button: Gtk.Button) -> None:
        self._add(state=None, direction=None, description=None, prepend=True)

    @property
    def description(self) -> Description:
        default: Optional[Description] = None
        states: Dict[str, Description] = {}

        for row in list(self.animations_box):
            if row.state == "default":
                default = row.description
                continue

            if row.state not in states:
                states[row.state] = Description(name=row.state, directions=[])

            states[row.state].directions.append(
                Description(
                    name=row.direction,
                    animation=row.description,
                )
            )

        return Description(
            default=default,
            states=list(states.values()),
        )

    @description.setter
    def description(self, description: Description) -> None:
        for row in list(self.animations_box):
            self._remove(row)

        if description.default is not None:
            self._add("default", None, description.default)

        for state in description.states:
            for direction in state.directions:
                self._add(state.name, direction.name, direction.animation)
