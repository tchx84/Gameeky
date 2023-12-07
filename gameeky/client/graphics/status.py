from typing import Optional

from gi.repository import Gdk, Gtk, Graphene

from ...common import colors


class Status:
    @classmethod
    def draw(
        cls,
        snapshot: Gtk.Snapshot,
        value: float,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Optional[Gdk.RGBA] = None,
    ) -> None:
        # Stroke

        rect_x = x
        rect_y = y
        rect_width = width
        rect_height = height

        stroke = Graphene.Rect()
        stroke.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(colors.BLACK, stroke)

        # Background

        offset = rect_height * 0.25

        rect_x += offset
        rect_y += offset
        rect_width -= offset * 2
        rect_height -= offset * 2

        background = Graphene.Rect()
        background.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(colors.WHITE, background)

        ## Fill

        rect_width *= value

        fill = Graphene.Rect()
        fill.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(color if color is not None else colors.GREEN, fill)
