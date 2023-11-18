#!/usr/bin/python

import os
import sys
import gi

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gdk, Gtk, Gio, Adw

from typing import Any, Optional

from .widgets.window import Window
from .widgets.session_new_window import SessionNewWindow
from .widgets.session_join_window import SessionJoinWindow
from .models.session import Session as SessionModel

from ..common.definitions import DEFAULT_ADDRESS


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Client",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        self._session_model: Optional[SessionModel] = None

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionNewWindow(transient_for=self._window)
        dialog.connect("done", self.__on_new_done)
        dialog.present()

    def __on_new_done(self, dialog: SessionNewWindow) -> None:
        self._shutdown_session()

        self._session_model = SessionModel(
            data_path=dialog.project_path,
            scene=dialog.scene_path,
            clients=dialog.players_value,
            address=DEFAULT_ADDRESS,
            session_port=dialog.session_port_value,
            messages_port=dialog.messages_port_value,
            scene_port=dialog.scene_port_value,
            stats_port=dialog.stats_port_value,
            host=True,
            window=self._window,
        )

        self._start_session()

    def __on_join(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionJoinWindow(transient_for=self._window)
        dialog.connect("done", self.__on_join_done)
        dialog.present()

    def __on_join_done(self, dialog: SessionNewWindow) -> None:
        self._shutdown_session()

        self._session_model = SessionModel(
            data_path=dialog.project_path,
            scene=None,
            clients=None,
            address=dialog.address_value,
            session_port=dialog.session_port_value,
            messages_port=dialog.messages_port_value,
            scene_port=dialog.scene_port_value,
            stats_port=dialog.stats_port_value,
            host=False,
            window=self._window,
        )

        self._start_session()

    def _start_session(self) -> None:
        if self._session_model is None:
            return

        self._session_model.connect("initializing", self.__on_session_initializing)
        self._session_model.connect("started", self.__on_session_started)
        self._session_model.connect("failed", self.__on_session_failed)
        self._session_model.create()

    def _shutdown_session(self) -> None:
        if self._session_model is not None:
            self._session_model.shutdown()

    def __on_session_initializing(self, model: SessionModel) -> None:
        self._window.switch_to_loading()

    def __on_session_started(self, model: SessionModel) -> None:
        self._window.switch_to_game(model.scene, model.stats)

    def __on_session_failed(self, model: SessionModel) -> None:
        self._window.switch_to_failed()

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

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        join_action = Gio.SimpleAction.new("join", None)
        join_action.connect("activate", self.__on_join)
        self.add_action(join_action)

    def do_shutdown(self) -> None:
        self._shutdown_session()
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
