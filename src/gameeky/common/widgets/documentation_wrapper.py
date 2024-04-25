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

import os
import locale

from gi.repository import Gtk, GLib

from ..utils import launch_path
from ..config import pkgdatadir


def present_documentation(window: Gtk.Window) -> None:
    try:
        from .documentation_window import DocumentationWindow
    except:
        launch_path(find_path())
    else:
        uri = GLib.filename_to_uri(find_path())

        dialog = DocumentationWindow(uri, transient_for=window)
        dialog.present()


def build_path(language: str) -> str:
    return os.path.join(pkgdatadir, "docs", "basics", "html", language, "index.html")


def find_path() -> str:
    code, encoding = locale.getlocale()

    if code is None:
        return build_path("en")
    elif os.path.exists((path := build_path(code))):
        return path
    elif os.path.exists((path := build_path(code.split("_")[0]))):
        return path

    return build_path("en")
