import math

from typing import Optional

from gi.repository import Gtk, Gdk, Graphene

from ...common.definitions import TILES_X, TILES_Y


class Highlight(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._color = Gdk.RGBA()
        self._color.parse("rgba(255,255,255,0.1)")

        self._highlight: Optional[Graphene.Rect] = None

        self._controller = Gtk.EventControllerMotion()
        self._controller.connect("motion", self.__on_moved)
        self._controller.connect("leave", self.__on_left)

        self.add_controller(self._controller)

    def __on_moved(
        self,
        controller: Gtk.EventControllerMotion,
        x: float,
        y: float,
    ) -> None:
        rect_width = self.get_width() / TILES_X
        rect_height = self.get_height() / TILES_Y

        rect_x = math.floor(x / rect_width) * rect_width
        rect_y = math.floor(y / rect_height) * rect_height

        self._highlight = Graphene.Rect()
        self._highlight.init(rect_x, rect_y, rect_width, rect_height)

        self.queue_draw()

    def __on_left(self, controller: Gtk.EventControllerMotion) -> None:
        self._highlight = None
        self.queue_draw()

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._highlight is None:
            return

        snapshot.append_color(self._color, self._highlight)
