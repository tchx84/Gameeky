from typing import Optional

from gi.repository import Gsk, Gdk, Gtk, Graphene

from ...client.graphics.entity import EntityRegistry


class Entity(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._type_id: Optional[int] = None

        self.visible = False
        self.props.hexpand = True
        self.props.vexpand = True

    def do_snapshot_entity(
        self,
        snapshot: Gtk.Snapshot,
        scale_x: float,
        scale_y: float,
        texture: Gdk.Texture,
    ) -> None:
        if texture is None:
            return

        ratio_x = 1.0 if scale_x >= scale_y else scale_x / scale_y
        ratio_y = 1.0 if scale_y >= scale_y else scale_y / scale_x

        rect_width = self.get_width() * ratio_x
        rect_height = self.get_height() * ratio_y

        rect_x = 0 if ratio_x == 1.0 else rect_width / 2
        rect_y = 0 if ratio_y == 1.0 else rect_height / 2

        rect = Graphene.Rect()
        rect.init(rect_x, rect_y, rect_width, rect_height)

        snapshot.append_scaled_texture(texture, Gsk.ScalingFilter.TRILINEAR, rect)

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._type_id is None:
            return

        scale_x, scale_y, texture = EntityRegistry.get_default_texture(self._type_id)
        self.do_snapshot_entity(snapshot, scale_x, scale_y, texture)

    @property
    def type_id(self) -> Optional[int]:
        return self._type_id

    @type_id.setter
    def type_id(self, type_id) -> None:
        self._type_id = type_id
        self.queue_draw()
