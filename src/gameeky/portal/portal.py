#!/usr/bin/python

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional

from gi.repository import Gio, Adw, Gdk, Gtk

from .widgets.window import Window
from .models.session import Session

from ..common.scanner import Description
from ..common.widgets.about_window import present_about


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.gameeky.Portal",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        self._session: Optional[Session] = None

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        self._window.add()

    def __on_about(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        present_about(self._window)

    def __on_found(self, session: Session, description: Description) -> None:
        self._window.load(description)

    def _setup_session(self) -> None:
        self._session = Session()
        self._session.connect("found", self.__on_found)
        self._session.scan()

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/dev/tchx84/gameeky/portal/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = Window(application=self)
        self._window.present()

        self._setup_session()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.__on_about)
        self.add_action(about_action)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main(version: str) -> None:
    application = Application()
    application.run(sys.argv)
