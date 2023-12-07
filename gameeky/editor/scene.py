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
from .widgets.scene_new_window import SceneNewWindow
from .widgets.scene_open_window import SceneOpenWindow
from .widgets.scene_edit_window import SceneEditWindow
from .models.scene_session import Session as SessionModel

from ..common.logger import logger
from ..common.utils import set_data_path, get_data_folder
from ..common.scanner import Description
from ..common.definitions import Format
from ..common.monitor import Monitor

from ..player.widgets.about_window import present_about


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.gameeky.editor.Scene",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        self._monitor = Monitor.default()
        self._data_path: Optional[str] = None
        self._description: Optional[Description] = None

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneNewWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_open(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneOpenWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_edit(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneEditWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.description = self._window.description
        dialog.present()

    def __on_done(self, dialog: SceneNewWindow) -> None:
        if (description := dialog.description) is None:
            return

        self._data_path = dialog.data_path
        self._description = description
        self._start_session()

    def _on_reload(self, window: SceneWindow) -> None:
        self._description = self._window.description
        self._start_session()

    def _start_session(self) -> None:
        set_data_path(self._data_path)

        self._window.reset()

        self._session_model = SessionModel()
        self._session_model.connect("registered", self.__on_session_registered)
        self._session_model.connect("ready", self.__on_session_ready)
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
    ) -> None:
        if self._description is not None:
            self._window.description = self._description

    def __on_save(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        folder = get_data_folder("scenes")

        json_filter = Gtk.FileFilter()
        json_filter.add_pattern(f"*.{Format.SCENE}")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.initial_name = self._window.suggested_name
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

    def __on_about(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        present_about(self._window)

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(__dir__, "style.css"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = SceneWindow(application=self)
        self._window.connect("reload", self._on_reload)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.__on_open)
        self.add_action(open_action)

        edit_action = Gio.SimpleAction.new("edit", None)
        edit_action.connect("activate", self.__on_edit)
        self.add_action(edit_action)

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.__on_save)
        self.add_action(save_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.__on_about)
        self.add_action(about_action)

    def do_shutdown(self) -> None:
        self._monitor.shutdown()
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
