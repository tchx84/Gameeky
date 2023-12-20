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


class AreaRow(BaseRow):
    __gtype_name__ = "AreaRowModel"

    __items__ = {
        "1x1": _("1x1"),
        "3x3": _("3x3"),
        "5x5": _("5x5"),
        "7x7": _("7x7"),
        "9x9": _("9x9"),
    }
