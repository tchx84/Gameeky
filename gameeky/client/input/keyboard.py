from typing import Dict, Optional

from gi.repository import Gdk, Gtk, GLib

from ..game.service import Service

from ...common.logger import logger
from ...common.utils import add_idle_source
from ...common.session import Session
from ...common.definitions import Action, Direction


class Keyboard(Gtk.EventControllerKey):
    action_by_key = {
        Gdk.KEY_Right: (Action.MOVE, Direction.EAST),
        Gdk.KEY_Up: (Action.MOVE, Direction.NORTH),
        Gdk.KEY_Left: (Action.MOVE, Direction.WEST),
        Gdk.KEY_Down: (Action.MOVE, Direction.SOUTH),
        Gdk.KEY_x: (Action.USE, 0),
        Gdk.KEY_c: (Action.TAKE, 0),
        Gdk.KEY_d: (Action.DROP, 0),
        Gdk.KEY_i: (Action.INTERACT, 0),
    }

    def __init__(
        self,
        widget: Gtk.Widget,
        service: Service,
        context: GLib.MainContext,
    ) -> None:
        super().__init__()
        self._is_pressed_by_key: Dict[int, bool] = {}
        self._registered_source_id: Optional[int] = None
        self._key_pressed_source_id: Optional[int] = None
        self._key_released_source_id: Optional[int] = None

        self._widget = widget
        self._widget.add_controller(self)

        self._service = service
        self._registered_source_id = self._service.connect(
            "registered",
            self.__on_service_registered,
        )

        self._context = context

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self._key_pressed_source_id = self.connect(
            "key-pressed",
            self.__on_key_pressed,
        )
        self._key_released_source_id = self.connect(
            "key-released",
            self.__on_key_released,
        )

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
        self._message(action, value)

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

        self._message(Action.IDLE, 0)

    def _message(self, action: Action, value: float) -> None:
        # Talk back to the service in the right context
        add_idle_source(self._service.message, (action, value), self._context)

    def shutdown(self) -> None:
        self._is_pressed_by_key = {}

        if self._key_pressed_source_id is not None:
            self.disconnect(self._key_pressed_source_id)
        if self._key_released_source_id is not None:
            self.disconnect(self._key_released_source_id)
        if self._registered_source_id is not None:
            self._service.disconnect(self._registered_source_id)

        self._widget.remove_controller(self)

        logger.info("Client.Keyboard.shut")
