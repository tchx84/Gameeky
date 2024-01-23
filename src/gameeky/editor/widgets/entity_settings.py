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

from gi.repository import Gtk, GObject

from .actuators_row import ActuatorsRow
from .dropdown_helper import DropDownHelper
from .change_signal_helper import ChangeSignalHelper

from ..models.direction_row import DirectionRow as DirectionRowModel
from ..models.state_row import StateRow as StateRowModel

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/entity_settings.ui")  # fmt: skip
class EntitySettings(Gtk.Box):
    __gtype_name__ = "EntitySettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    name = Gtk.Template.Child()
    target_name = Gtk.Template.Child()
    dialogue = Gtk.Template.Child()
    stamina = Gtk.Template.Child()
    durability = Gtk.Template.Child()
    weight = Gtk.Template.Child()
    strength = Gtk.Template.Child()
    target_type = Gtk.Template.Child()
    radius = Gtk.Template.Child()
    rate = Gtk.Template.Child()
    recovery = Gtk.Template.Child()
    density = Gtk.Template.Child()
    luminance = Gtk.Template.Child()
    removable = Gtk.Template.Child()
    takeable = Gtk.Template.Child()
    usable = Gtk.Template.Child()
    visible = Gtk.Template.Child()
    direction = Gtk.Template.Child()
    state = Gtk.Template.Child()
    actuators = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._actuators = ActuatorsRow()
        self.actuators.props.child = self._actuators

        self._direction = DropDownHelper(self.direction, DirectionRowModel)
        self._state = DropDownHelper(self.state, StateRowModel)

        self._changes = ChangeSignalHelper(self.__on_changed)
        self._changes.add(self.stamina)
        self._changes.add(self.durability)
        self._changes.add(self.weight)
        self._changes.add(self.strength)
        self._changes.add(self.recovery)
        self._changes.add(self.density)
        self._changes.add(self.name)
        self._changes.add(self.target_name)
        self._changes.add(self.dialogue)
        self._changes.add(self.target_type)
        self._changes.add(self.radius)
        self._changes.add(self.rate)
        self._changes.add(self._actuators)
        self._changes.add(self.visible, signal="notify::active")
        self._changes.add(self.luminance)
        self._changes.add(self._state)
        self._changes.add(self._direction)
        self._changes.add(self.removable, signal="notify::active")
        self._changes.add(self.takeable, signal="notify::active")
        self._changes.add(self.usable, signal="notify::active")

    def __on_changed(self, *args) -> None:
        self.emit("changed")

    @property
    def description(self) -> Description:
        return Description(
            name=self.name.props.text,
            target_name=self.target_name.props.text,
            dialogue=self.dialogue.props.text,
            stamina=int(self.stamina.props.value),
            durability=int(self.durability.props.value),
            weight=int(self.weight.props.value),
            strength=int(self.strength.props.value),
            target_type=int(self.target_type.props.value),
            radius=int(self.radius.props.value),
            rate=int(self.rate.props.value),
            recovery=round(self.recovery.props.value, 2),
            density=round(self.density.props.value, 2),
            luminance=round(self.luminance.props.value, 2),
            removable=self.removable.props.active,
            takeable=self.takeable.props.active,
            usable=self.usable.props.active,
            visible=self.visible.props.active,
            direction=self._direction.value,
            state=self._state.value,
            actuators=self._actuators.value,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self._changes.block()

        self.name.props.text = description.name
        self.target_name.props.text = description.target_name
        self.dialogue.props.text = description.dialogue
        self.stamina.props.value = description.stamina
        self.durability.props.value = description.durability
        self.weight.props.value = description.weight
        self.strength.props.value = description.strength
        self.target_type.props.value = description.target_type
        self.radius.props.value = description.radius
        self.rate.props.value = description.rate
        self.recovery.props.value = description.recovery
        self.density.props.value = description.density
        self.luminance.props.value = description.luminance
        self.removable.props.active = description.removable
        self.takeable.props.active = description.takeable
        self.usable.props.active = description.usable
        self.visible.props.active = description.visible
        self._direction.value = description.direction
        self._state.value = description.state
        self._actuators.value = description.actuators

        self._changes.unblock()
