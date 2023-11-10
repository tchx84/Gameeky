from typing import Optional, Tuple

from gi.repository import Gsk, Gtk, Gdk, Graphene, Pango

from ...common import colors
from ...common.utils import get_data_path, clamp


class Tileset(Gtk.Widget):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._rows = 1
        self._columns = 1
        self._scale = 1.0
        self._path = ""
        self._texture: Optional[Gdk.Texture] = None

        self.props.hexpand = True
        self.props.vexpand = True
        self.props.halign = Gtk.Align.CENTER
        self.props.valign = Gtk.Align.CENTER

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
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

        rect_width = width / self._columns
        rect_height = height / self._rows

        border_size = Graphene.Size()
        border_size.init(1, 1)

        index = 0

        for row in range(0, self._rows):
            for column in range(0, self._columns):
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

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE

    def do_measure(
        self,
        orientation: Gtk.Orientation,
        for_size: int,
    ) -> Tuple[float, ...]:
        if self._texture is None:
            return (0, 0, -1, -1)

        if orientation == Gtk.Orientation.HORIZONTAL:
            width = self._texture.get_intrinsic_width() * self.scale
            return (width, width, -1, -1)
        else:
            height = self._texture.get_intrinsic_height() * self.scale
            return (height, height, -1, -1)

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, rows: int) -> None:
        self._rows = rows
        self.queue_draw()

    @property
    def columns(self) -> int:
        return self._columns

    @columns.setter
    def columns(self, columns: int) -> None:
        self._columns = columns
        self.queue_draw()

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        self._path = path
        self._texture = Gdk.Texture.new_from_filename(get_data_path(self._path))
        self.queue_draw()

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        self._scale = clamp(10, 1.0, scale)
        self.queue_resize()
