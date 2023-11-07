#!/usr/bin/python

import sys
import gi
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw, Gdk, Gtk

from .widgets.window import Window


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Editor",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(__dir__, "style.css"))
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


def main() -> None:
    application = Application()
    application.run(sys.argv)
