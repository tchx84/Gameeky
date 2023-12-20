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


class LayerRow(BaseRow):
    __gtype_name__ = "LayerRowModel"

    __items__ = {
        "layer 0": _("Layer 0"),
        "layer 1": _("Layer 1"),
        "layer 2": _("Layer 2"),
        "layer 3": _("Layer 3"),
        "layer 4": _("Layer 4"),
        "layer 5": _("Layer 5"),
        "layer 6": _("Layer 6"),
        "layer 7": _("Layer 7"),
        "all layers": _("All layers"),
    }
