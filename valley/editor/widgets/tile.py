from typing import Optional

from gi.repository import Gsk, Gtk, Gdk, Graphene, Pango

from ...common import colors
from ...common.utils import get_data_path
from ...common.scanner import Description


class Tile(Gtk.Widget):
    __gtype_name__ = "Tile"

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._description: Optional[Description] = None
        self._texture: Optional[Gdk.Texture] = None
        self.set_hexpand(True)
        self.set_vexpand(True)

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._description is None:
            return
        if self._texture is None:
            return

        width = self.get_width()
        height = self.get_height()

        rect = Graphene.Rect()
        rect.init(0, 0, width, height)

        snapshot.append_scaled_texture(self._texture, Gsk.ScalingFilter.TRILINEAR, rect)

        font = Pango.FontDescription.new()
        font.set_family("Sans")
        font.set_size(12 * Pango.SCALE)

        context = self.get_pango_context()
        layout = Pango.Layout(context)
        layout.set_font_description(font)

        rect_width = width / self._description.columns
        rect_height = height / self._description.rows

        border_size = Graphene.Size()
        border_size.init(1, 1)

        index = 0

        for row in range(0, self._description.rows):
            for column in range(0, self._description.columns):
                snapshot.save()

                x = column * rect_width
                y = row * rect_height

                border_rect = Graphene.Rect()
                border_rect.init(x, y, rect_width, rect_height)

                border = Gsk.RoundedRect()
                border.init(
                    border_rect,
                    border_size,
                    border_size,
                    border_size,
                    border_size,
                )

                snapshot.append_border(
                    border,
                    [1.0, 1.0, 1.0, 1.0],
                    [colors.GREEN, colors.GREEN, colors.GREEN, colors.GREEN],
                )

                position = Graphene.Point()
                position.x = x
                position.y = y

                snapshot.translate(position)

                layout.set_text(f"{index}")
                snapshot.append_layout(layout, colors.GREEN)
                index += 1

                snapshot.restore()

    def update(self, description: Description) -> None:
        self._description = description
        self._texture = Gdk.Texture.new_from_filename(get_data_path(description.path))
        self.queue_draw()
