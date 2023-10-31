from gi.repository import Gdk, Gtk

from typing import Optional

from ...graphics.status import Status as StatusGraphics


class Status(Gtk.Widget):
    def __init__(self, color: Optional[Gdk.RGBA] = None) -> None:
        super().__init__()
        self._value = 0.0
        self._color = color

        self.props.vexpand = True
        self.props.hexpand = True

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        width = self.get_width()
        height = self.get_height()

        StatusGraphics.draw(
            snapshot,
            self._value,
            0,
            0,
            width,
            height,
            width,
            height,
            self._color,
        )

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value
        self.queue_draw()
