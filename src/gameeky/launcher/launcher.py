#!/usr/bin/python
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


import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional
from gettext import gettext as _

from gi.repository import GLib, Gio, Adw, Gdk, Gtk

from .widgets.window import Window
from .widgets.confirmation_create_window import ConfirmationCreateWindow
from .models.session import Session
from .models.service import Software

from ..common.scanner import Description
from ..common.widgets.about_window import present_about
from ..common.widgets.documentation_wrapper import present_documentation


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.Gameeky.Launcher",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        GLib.set_application_name(_("Gameeky"))

        self._session: Optional[Session] = None

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        if Software.available():
            dialog = ConfirmationCreateWindow(transient_for=self._window)
            dialog.connect("confirmed", self.__on_create_confirmed)
            dialog.present()
        else:
            self._window.add()

    def __on_create_confirmed(self, dialog: ConfirmationCreateWindow) -> None:
        self._window.add()

    def __on_about(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        present_about(self._window)

    def __on_documentation(
        self,
        action: Gio.SimpleAction,
        data: Optional[Any] = None,
    ) -> None:
        present_documentation(self._window)

    def __on_found(self, session: Session, path: str, description: Description) -> None:
        self._window.load(path, description)

    def __on_reload(self, window: Window) -> None:
        self._window.reset()
        self._setup_session()

    def _setup_session(self) -> None:
        self._session = Session()
        self._session.connect("found", self.__on_found)
        self._session.scan()

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/dev/tchx84/gameeky/launcher/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = Window(application=self)
        self._window.connect("reload", self.__on_reload)
        self._window.present()

        self._setup_session()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        documentation_action = Gio.SimpleAction.new("documentation", None)
        documentation_action.connect("activate", self.__on_documentation)
        self.add_action(documentation_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.__on_about)
        self.add_action(about_action)

    def do_shutdown(self) -> None:
        if self._session is not None:
            self._session.shutdown()
        Adw.Application.do_shutdown(self)


def main(version: str) -> None:
    application = Application()
    application.run(sys.argv)
