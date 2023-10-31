from gi.repository import Gtk

from ...graphics.status import Status as StatusGraphics


class Status(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._value = 0.0

        self.props.vexpand = True
        self.props.hexpand = True

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        width = self.get_width()
        height = self.get_height()

        StatusGraphics.draw(snapshot, self._value, 0, 0, width, height, width, height)

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value
        self.queue_draw()
