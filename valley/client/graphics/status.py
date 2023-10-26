from gi.repository import Gdk, Gtk, Graphene

from ...common.entity import Entity


class Status:
    fill = Gdk.RGBA()
    fill.parse("#74D600")

    background = Gdk.RGBA()
    background.parse("#FFFFFF")

    stroke = Gdk.RGBA()
    stroke.parse("#000000")

    @classmethod
    def draw(
        cls,
        snapshot: Gtk.Snapshot,
        entity: Entity,
        x: float,
        y: float,
        width: float,
        height: float,
        target_width: float,
        target_height: float,
    ) -> None:
        if entity.status == 1.0:
            return

        # Stroke

        rect_x = x + (width / 2) - (target_width / 2)
        rect_y = y
        rect_width = target_width
        rect_height = target_height * 0.2

        stroke = Graphene.Rect()
        stroke.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(cls.stroke, stroke)

        # Background

        offset = rect_height * 0.25

        rect_x += offset
        rect_y += offset
        rect_width -= offset * 2
        rect_height -= offset * 2

        background = Graphene.Rect()
        background.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(cls.background, background)

        ## Fill

        rect_width *= entity.status

        fill = Graphene.Rect()
        fill.init(rect_x, rect_y, rect_width, rect_height)
        snapshot.append_color(cls.fill, fill)
