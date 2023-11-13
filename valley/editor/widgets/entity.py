from typing import Optional

from gi.repository import Gsk, Gtk, Graphene

from ...client.graphics.entity import EntityRegistry


class Entity(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._type_id: Optional[int] = None

        self.visible = False
        self.props.hexpand = True
        self.props.vexpand = True

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self.visible is False:
            return
        if self._type_id is None:
            return

        _, _, texture = EntityRegistry.get_default_texture(self._type_id)

        if texture is None:
            return

        rect = Graphene.Rect()
        rect.init(0, 0, self.get_width(), self.get_height())

        snapshot.append_scaled_texture(texture, Gsk.ScalingFilter.TRILINEAR, rect)

    @property
    def type_id(self) -> Optional[int]:
        return self._type_id

    @type_id.setter
    def type_id(self, type_id) -> None:
        self._type_id = type_id
        self.queue_draw()
