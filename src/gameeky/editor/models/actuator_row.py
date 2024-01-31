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

from typing import Optional, List
from gettext import gettext as _

from gi.repository import Gio

from .base_row import BaseRow

from ...server.game.actuators.base import ActuatorRegistry


class ActuatorRow(BaseRow):
    __gtype_name__ = "ActuatorRowModel"

    __items__ = {
        "activates": _("Activates"),
        "activates_i": _("Activates on interaction"),
        "affects": _("Affects"),
        "affects_i": _("Affects on interaction"),
        "affects_u": _("Affects on use"),
        "aggroes": _("Aggroes"),
        "collapses": _("Collapses"),
        "collapses_t": _("Collapses over time"),
        "destroys": _("Destroys"),
        "destroys_i": _("Destroys on interaction"),
        "deteriorates": _("Deteriorates"),
        "drops": _("Drops"),
        "exhausts": _("Exhausts"),
        "follows": _("Follows"),
        "interacts": _("Interacts"),
        "propulses": _("Propulses"),
        "requires": _("Requires"),
        "roams": _("Roams"),
        "rotates_i": _("Rotates on interaction"),
        "says": _("Says"),
        "says_i": _("Says on interaction"),
        "spawns": _("Spawns"),
        "takes": _("Takes"),
        "targets": _("Targets"),
        "teleports": _("Teleports"),
        "teleports_i": _("Teleports on interaction"),
        "transmutes": _("Transmutes"),
        "triggers": _("Triggers"),
        "triggers_i": _("Triggers on interaction"),
        "uses": _("Uses"),
    }

    __tooltips__ = {
        "activates": _("Activates entities in its position"),
        "activates_i": _("Activates entities in its position, when it's interacted with"),
        "affects": _("Affects the stats (Durability, Stamina and Strength) of nearby (Radius) entities"),
        "affects_i": _("Affects the stats (Durability, Stamina and Strength) of its interactees"),
        "affects_u": _("Affects the stats of nearby (Radius) entities, when it's used"),
        "aggroes": _("Targets nearby (Radius) entities (Target Type)"),
        "collapses": _("Performs a DESTROY action, when entities are nearby (Radius)"),
        "collapses_t": _("Performs a DESTROY action on a fixed interval (Rate)"),
        "destroys": _("Performs a DESTROY action, when its stamina reaches zero"),
        "destroys_i": _("Performs a DESTROY action, when it's interacted with"),
        "deteriorates": _("Reduces its durability over time"),
        "drops": _("Adds entities (Target Type) to the scene, when destroyed"),
        "exhausts": _("Performs an EXHAUST action, when its stamina reaches zero"),
        "follows": _("Performs a MOVE action to its target (Target Name) direction"),
        "interacts": _("Performs an INTERACT action on entities (Target Type)"),
        "propulses": _("Performs an MOVE action at its direction"),
        "requires": _("Activates its target (Target Name), when its requirement (Target Type) is in its position"),
        "roams": _("Performs a MOVE action at random directions"),
        "rotates_i": _("Rotates, when it's interacted with"),
        "says": _("Sends its dialogue nearby (Radius) entities"),
        "says_i": _("Sends its dialogue to its interactees"),
        "spawns": _("Adds entities (Target Type) to the scene on a fixed interval (Rate)"),
        "takes": _("Performs a TAKE action on targets (Target Type)"),
        "targets": _("Targets its target's target, when reaching its target position"),
        "teleports": _("Teleports nearby (Radius) entities to a fixed position (Target Name)"),
        "teleports_i": _("Teleports interactees to a fixed position (Target Name)"),
        "transmutes": _("Replaces itself by its target (Target Type) on a fixed interval (Rate)"),
        "triggers": _("Activates its target (Target Name), when entities are nearby (Radius)"),
        "triggers_i": _("Activates its target (Target Name), when it's interacted with"),
        "uses": _("Performs a USE action, when holding an usable entity"),
    }  # fmt: skip

    @classmethod
    def model(cls, default=False, exclude: Optional[List[str]] = None) -> Gio.ListStore:
        model = super().model()

        for value in ActuatorRegistry.names():
            model.append(cls(value=value, text=value, tooltip=""))

        return model
