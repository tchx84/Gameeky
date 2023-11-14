#!/usr/bin/python

import sys
import gi
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw

from .widgets.scene_window import SceneWindow
from .models.entity import Entity as EntityModel

from ..common.utils import get_data_path
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

    def __on_model_finished(self, model: EntityModel) -> None:
        self._window.description = Description.new_from_json(
            get_data_path("scenes/default.json"),
        )

    def do_activate(self) -> None:
        self._window = SceneWindow(application=self)
        self._window.present()

        self._entity_model = EntityModel()
        self._entity_model.connect("registered", self.__on_model_registered)
        self._entity_model.connect("finished", self.__on_model_finished)
        self._entity_model.scan()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
