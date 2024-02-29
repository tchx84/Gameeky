#!/usr/bin/python
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


import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gettext import gettext as _

from gi.repository import GLib, Gio, Adw, Gdk, Gtk

from .widgets.window import Window


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.Gameeky.Coder",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        GLib.set_application_name(_("Coder"))

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/dev/tchx84/gameeky/library/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = Window(application=self)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main(version: str) -> None:
    application = Application()
    application.run(sys.argv)
