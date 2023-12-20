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

from typing import Dict, List, Optional
from gettext import gettext as _

from gi.repository import Gio, GObject


class BaseRow(GObject.GObject):
    __gtype_name__ = "BaseRowModel"

    __items__: Dict[str, str] = {}

    value = GObject.Property(type=str)
    text = GObject.Property(type=str)

    def __init__(self, value: str, text: str) -> None:
        super().__init__()
        self.value = value
        self.text = text

    @classmethod
    def model(cls, default=False, exclude: Optional[List[str]] = None) -> Gio.ListStore:
        model = Gio.ListStore()

        if default is True:
            model.append(cls(value="default", text=_("Default")))

        for value, text in cls.__items__.items():
            if exclude is not None and value in exclude:
                continue
            model.append(cls(value=value, text=text))

        return model
