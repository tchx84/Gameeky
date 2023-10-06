from gi.repository import GObject, Gdk, Gtk

from ...common.action import Action
from ...common.direction import Direction


class Keyboard(Gtk.EventControllerKey):
    __gsignals__ = {
        "enacted": (GObject.SignalFlags.RUN_LAST, None, (int, float)),
    }

    MAPPING = {
        Gdk.KEY_Right: (Action.MOVE, Direction.RIGHT),
        Gdk.KEY_Up: (Action.MOVE, Direction.UP),
        Gdk.KEY_Left: (Action.MOVE, Direction.LEFT),
        Gdk.KEY_Down: (Action.MOVE, Direction.DOWN),
    }

    def __init__(self, widget: Gtk.Widget) -> None:
        super().__init__()

        self._widget = widget
        self._widget.add_controller(self)

        self.connect("key-pressed", self.__on_key_pressed)

    def __on_key_pressed(
        self,
        controller: Gtk.EventControllerKey,
        key: int,
        code: int,
        state: Gdk.ModifierType,
    ):
        action, value = self.MAPPING.get(key, (None, None))

        if action is not None:
            self.emit("enacted", action, value)

        return True
