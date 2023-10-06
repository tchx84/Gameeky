#!/usr/bin/python

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk, GLib

from valley.client.game.service import Service
from valley.client.game.scene import Scene as SceneModel
from valley.client.graphics.scene import Scene as SceneView
from valley.client.input.keyboard import Keyboard as Input

SESSION_PORT = 9998
UPDATES_PORT = 9997
SCENE_PORT = 9999
ADDRESS = "127.0.0.1"


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self._setup_game()
        self._setup_graphics()
        self._setup_input()

    def _setup_input(self):
        self._input = Input(self)
        self._input.connect("enacted", self.__on_enacted)

    def _setup_graphics(self):
        self.set_title("Valley")
        self._view = SceneView(model=self._model)
        self.set_child(self._view)

    def _setup_game(self):
        self._model = SceneModel()

        self._service = Service(
            address=ADDRESS,
            session_port=SESSION_PORT,
            updates_port=UPDATES_PORT,
            scene_port=SCENE_PORT,
            context=GLib.MainContext.default(),
        )
        self._service.connect("registered", self.__on_registered)
        self._service.register()

    def __on_registered(self, service, session):
        self._model.anchor_id = session.entity_id
        self._model.connect("ticked", self.__on_ticked)
        self._service.connect("updated", self.__on_updated)

    def __on_ticked(self, model):
        self._service.request()

    def __on_updated(self, service, model):
        self._model.update(model)
        self._view.queue_draw()

    def __on_enacted(self, input, action, value):
        self._service.report(action, value)


def on_activate(app):
    win = Window(app)
    win.present()


app = Gtk.Application(
    application_id="dev.tchx84.Valley",
    flags=Gio.ApplicationFlags.NON_UNIQUE,
)
app.connect("activate", on_activate)
app.run(None)
