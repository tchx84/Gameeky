#!/usr/bin/python

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw

from .widgets.window import Window


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Editor",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

    def do_activate(self) -> None:
        self._window = Window(application=self)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
