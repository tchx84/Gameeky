from typing import Dict

from gi.repository import GObject, Gdk, Gtk

from ...common.action import Action
from ...common.direction import Direction


class Keyboard(Gtk.EventControllerKey):
    __gsignals__ = {
        "performed": (GObject.SignalFlags.RUN_LAST, None, (int, float)),
    }

    action_by_key = {
        Gdk.KEY_Right: (Action.MOVE, Direction.RIGHT),
        Gdk.KEY_Up: (Action.MOVE, Direction.UP),
        Gdk.KEY_Left: (Action.MOVE, Direction.LEFT),
        Gdk.KEY_Down: (Action.MOVE, Direction.DOWN),
    }

    def __init__(self, widget: Gtk.Widget) -> None:
        super().__init__()
        self._is_pressed_by_key: Dict[int, bool] = {}

        self._widget = widget
        self._widget.add_controller(self)

        self.connect("key-pressed", self.__on_key_pressed)
        self.connect("key-released", self.__on_key_released)

    def __on_key_pressed(
        self,
        controller: Gtk.EventControllerKey,
        key: int,
        code: int,
        state: Gdk.ModifierType,
    ):
        if self._is_pressed_by_key.get(key) is True:
            return

        action, value = self.action_by_key.get(key, (None, None))
        if action is None:
            return

        self._is_pressed_by_key[key] = True
        self.emit("performed", action, value)

    def __on_key_released(
        self,
        controller: Gtk.EventControllerKey,
        key: int,
        code: int,
        state: Gdk.ModifierType,
    ):
        action, _ = self.action_by_key.get(key, (None, None))
        if action is None:
            return

        if self._is_pressed_by_key.get(key):
            del self._is_pressed_by_key[key]
        if self._is_pressed_by_key.keys():
            return

        self.emit("performed", Action.NOTHING, 0)
