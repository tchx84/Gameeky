#!/usr/bin/python

import sys
import gi
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional

from gi.repository import Gio, Gtk, Adw

from .widgets.scene_window import SceneWindow
from .models.entity import Entity as EntityModel

from ..common.logger import logger
from ..common.scanner import Description


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.editor.Scene",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

    def __on_model_registered(
        self, model: EntityModel, description: Description
    ) -> None:
        self._window.register(description)

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
            return

        self._window.description = Description.new_from_json(file.get_path())

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
        self._window = SceneWindow(application=self)
        self._window.present()

        self._entity_model = EntityModel()
        self._entity_model.connect("registered", self.__on_model_registered)
        self._entity_model.scan()

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
