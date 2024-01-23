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

    @classmethod
    def model(cls, default=False, exclude: Optional[List[str]] = None) -> Gio.ListStore:
        model = super().model()

        for value in ActuatorRegistry.names():
            model.append(cls(value=value, text=value))

        return model
