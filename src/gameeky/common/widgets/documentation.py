# Copyright (c) 2024 Martín Abente Lahaye.
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

import locale

from gi.repository import Gio

from ..config import VERSION

URL = "https://github.com/tchx84/Gameeky/blob/v%s/docs/basics/%s/%s.md"

SUPPORTED = {
    "en_": {"language": "en", "document": "welcome"},
}


def present_documentation() -> None:
    supported = SUPPORTED["en_"]
    code, encode = locale.getlocale()

    if code is not None:
        for option in SUPPORTED:
            if code.startswith(option):
                supported = SUPPORTED[option]

    Gio.AppInfo.launch_default_for_uri(
        URL % (VERSION, supported["language"], supported["document"]),
        None,
    )
