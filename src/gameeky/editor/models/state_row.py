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

from gettext import gettext as _

from .base_row import BaseRow


class StateRow(BaseRow):
    __gtype_name__ = "StateRowModel"

    __items__ = {
        "destroyed": _("Destroyed"),
        "destroying": _("Destroying"),
        "dropping": _("Dropping"),
        "exhausted": _("Exhausted"),
        "held": _("Held"),
        "idling": _("Idling"),
        "interacting": _("Interacting"),
        "moving": _("Moving"),
        "taking": _("Taking"),
        "using": _("Using"),
    }
