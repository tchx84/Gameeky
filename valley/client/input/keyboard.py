from typing import Dict

from gi.repository import Gdk, Gtk

from ..game.service import Service

from ...common.action import Action
from ...common.session import Session
from ...common.direction import Direction


class Keyboard(Gtk.EventControllerKey):
    action_by_key = {
        Gdk.KEY_Right: (Action.MOVE, Direction.RIGHT),
        Gdk.KEY_Up: (Action.MOVE, Direction.UP),
        Gdk.KEY_Left: (Action.MOVE, Direction.LEFT),
        Gdk.KEY_Down: (Action.MOVE, Direction.DOWN),
        Gdk.KEY_x: (Action.USE, 0),
        Gdk.KEY_c: (Action.TAKE, 0),
        Gdk.KEY_d: (Action.DROP, 0),
    }

    def __init__(self, widget: Gtk.Widget, service: Service) -> None:
        super().__init__()
        self._is_pressed_by_key: Dict[int, bool] = {}

        self._widget = widget
        self._widget.add_controller(self)

        self._service = service
        self._service.connect("registered", self.__on_service_registered)

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self.connect("key-pressed", self.__on_key_pressed)
        self.connect("key-released", self.__on_key_released)

    def __on_key_pressed(
        self,
        controller: Gtk.EventControllerKey,
        key: int,
        code: int,
        state: Gdk.ModifierType,
    ) -> None:
        if self._is_pressed_by_key.get(key) is True:
            return

        action, value = self.action_by_key.get(key, (None, 0))
        if action is None:
            return

        self._is_pressed_by_key[key] = True
        self._service.message(action, value)

    def __on_key_released(
        self,
        controller: Gtk.EventControllerKey,
        key: int,
        code: int,
        state: Gdk.ModifierType,
    ) -> None:
        action, _ = self.action_by_key.get(key, (None, None))
        if action is None:
            return

        if self._is_pressed_by_key.get(key):
            del self._is_pressed_by_key[key]
        if self._is_pressed_by_key.keys():
            return

        self._service.message(Action.IDLE, 0)
