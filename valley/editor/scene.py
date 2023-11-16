#!/usr/bin/python

import sys
import gi
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional

from gi.repository import Gdk, Gio, Gtk, Adw

from .widgets.scene_window import SceneWindow
from .widgets.scene_creation_window import SceneCreationWindow
from .widgets.scene_open_window import SceneOpenWindow
from .models.session import Session as SessionModel

from ..common.logger import logger
from ..common.utils import set_data_path
from ..common.scanner import Description


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.editor.Scene",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneCreationWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_open(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneOpenWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_done(self, dialog: SceneCreationWindow) -> None:
        if (description := dialog.description) is None:
            return

        set_data_path(dialog.data_path)

        self._window.reset()

        self._session_model = SessionModel()
        self._session_model.connect("registered", self.__on_session_registered)
        self._session_model.connect("ready", self.__on_session_ready, description)
        self._session_model.scan()

    def __on_session_registered(
        self,
        model: SessionModel,
        description: Description,
    ) -> None:
        self._window.register(description)

    def __on_session_ready(
        self,
        model: SessionModel,
        description: Description,
    ) -> None:
        self._window.description = description

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
            return

        file = Gio.File.new_for_path(file.get_path())
        file.replace_contents(
            contents=self._window.description.to_json().encode("UTF-8"),
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.REPLACE_DESTINATION,
            cancellable=None,
        )

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(__dir__, "style.css"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = SceneWindow(application=self)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

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
