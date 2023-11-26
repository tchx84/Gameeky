import math

from typing import Tuple

from gi.repository import Gtk, Graphene, GObject

from ...common import colors
from ...common.vector import Vector
from ...common.utils import clamp


class Grid(Gtk.Widget):
    __gsignals__ = {
        "clicked": (GObject.SignalFlags.RUN_LAST, None, (int, int)),
    }

    TILE_SIZE = 10

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._rows = 0
        self._columns = 0
        self._scale = 1.0
        self._highlight = Vector()

        self._controller = Gtk.GestureClick()
        self._controller.connect("pressed", self.__on_clicked)
        self.add_controller(self._controller)

        self.props.hexpand = True
        self.props.vexpand = True

    def __on_clicked(
        self,
        controller: Gtk.GestureClick,
        n_press: int,
        x: float,
        y: float,
    ) -> None:
        if not self.ready:
            return

        width = self.get_width()
        height = self.get_height()

        tile_width = math.floor(width / self._columns)
        tile_height = math.floor(height / self._rows)

        offset_x = (width - (tile_width * self._columns)) / 2
        offset_y = (height - (tile_height * self._rows)) / 2

        tile_x = (x - offset_x) / tile_width
        tile_y = (y - offset_y) / tile_height

        self.emit("clicked", tile_x, tile_y)

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if not self.ready:
            return

        width = self.get_width()
        height = self.get_height()

        rect_width = math.floor(width / self._columns)
        rect_height = math.floor(height / self._rows)

        offset_x = (width - (rect_width * self._columns)) / 2
        offset_y = (height - (rect_height * self._rows)) / 2

        x = (self.highlight.x * rect_width) + offset_x
        y = (self.highlight.y * rect_height) + offset_y

        highlight_rect = Graphene.Rect()
        highlight_rect.init(x, y, rect_width, rect_height)

        snapshot.append_color(colors.GREEN, highlight_rect)

        for column in range(0, self._columns + 1):
            x = (column * rect_width) + offset_x

            line = Graphene.Rect()
            line.init(x, offset_y, 1, height - (offset_y * 2))

            snapshot.append_color(colors.GREEN, line)

        for row in range(0, self._rows + 1):
            y = (row * rect_height) + offset_y

            line = Graphene.Rect()
            line.init(offset_x, y, width - (offset_x * 2), 1)

            snapshot.append_color(colors.GREEN, line)

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE

    def do_measure(
        self,
        orientation: Gtk.Orientation,
        for_size: int,
    ) -> Tuple[float, ...]:
        if orientation == Gtk.Orientation.HORIZONTAL:
            width = self._columns * self.TILE_SIZE * self.scale
            return (width, width, -1, -1)
        else:
            height = self._rows * self.TILE_SIZE * self.scale
            return (height, height, -1, -1)

    @property
    def ready(self) -> bool:
        return self._rows > 0 and self._columns > 0

    @property
    def highlight(self) -> Vector:
        return self._highlight

    @highlight.setter
    def highlight(self, highlight: Vector) -> None:
        self._highlight = highlight
        self.queue_draw()

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, rows: int) -> None:
        self._rows = rows
        self.queue_resize()

    @property
    def columns(self) -> int:
        return self._columns

    @columns.setter
    def columns(self, columns: int) -> None:
        self._columns = columns
        self.queue_resize()

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        self._scale = clamp(10, 1.0, scale)
        self.queue_resize()
