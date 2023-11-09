#!/usr/bin/python

import sys
import gi
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional

from gi.repository import Gio, Adw, Gdk, Gtk

from .widgets.window import Window

from ..common.logger import logger


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Editor",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

    def __on_open(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        json_filter = Gtk.FileFilter()
        json_filter.add_pattern("*.json")

        dialog = Gtk.FileDialog()
        dialog.props.default_filter = json_filter
        dialog.open(callback=self.__on_open_finished)

    def __on_open_finished(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self._window.open(file.get_path())

    def __on_save(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        json_filter = Gtk.FileFilter()
        json_filter.add_pattern("*.json")

        dialog = Gtk.FileDialog()
        dialog.props.default_filter = json_filter
        dialog.save(callback=self.__on_save_finished)

    def __on_save_finished(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.save_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self._window.save(file.get_path())

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

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.__on_open)
        self.add_action(open_action)

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.__on_save)
        self.add_action(save_action)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
