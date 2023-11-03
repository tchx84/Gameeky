#!/usr/bin/python

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw

from typing import Any, Optional

from .widgets.window import Window
from .widgets.session import Session as SessionDialog
from .models.session import Session as SessionModel

from ..client.sound.scene import Scene as SceneSound


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Client",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

        self._session_model: Optional[SessionModel] = None
        self._sound_player = SceneSound()

    def __on_create(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionDialog(host=True, transient_for=self._window)
        dialog.connect("done", self.__on_session_dialog_done)
        dialog.present()

    def __on_join(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionDialog(host=False, transient_for=self._window)
        dialog.connect("done", self.__on_session_dialog_done)
        dialog.present()

    def __on_session_dialog_done(self, dialog: SessionDialog) -> None:
        self._shutdown_session()
        self._session_model = SessionModel(
            scene=dialog.scene,
            clients=dialog.clients,
            address=dialog.address,
            session_port=dialog.session_port,
            messages_port=dialog.messages_port,
            scene_port=dialog.scene_port,
            stats_port=dialog.stats_port,
            host=dialog.host,
            window=self._window,
        )
        self._session_model.connect(
            "initializing", self.__on_session_model_initializing
        )
        self._session_model.connect("started", self.__on_session_model_started)
        self._session_model.connect("failed", self.__on_session_model_failed)
        self._session_model.create()

    def __on_session_model_initializing(self, model: SessionModel) -> None:
        self._window.switch_to_loading()

    def __on_session_model_started(self, model: SessionModel) -> None:
        self._window.switch_to_game(model.scene, model.stats)
        self._sound_player.model = model.scene

    def __on_session_model_failed(self, model: SessionModel) -> None:
        self._window.switch_to_game(None, None)
        self._sound_player.model = None

    def _shutdown_session(self) -> None:
        if self._session_model is not None:
            self._session_model.shutdown()

    def do_activate(self) -> None:
        self._window = Window(application=self)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        create_action = Gio.SimpleAction.new("create", None)
        create_action.connect("activate", self.__on_create)
        self.add_action(create_action)

        join_action = Gio.SimpleAction.new("join", None)
        join_action.connect("activate", self.__on_join)
        self.add_action(join_action)

    def do_shutdown(self) -> None:
        self._shutdown_session()
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
