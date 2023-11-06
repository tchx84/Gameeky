from typing import Optional

from gi.repository import Gsk, Gtk, GLib, Graphene

from ...common.scanner import Description
from ...common.definitions import TICK

from ...client.graphics.entity import Animation, EntityRegistry


class EntityRenderer(Gtk.Widget):
    __gtype_name__ = "Entity"

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._animation: Optional[Animation] = None
        self._handler_id = GLib.timeout_add(TICK, self.__on_entity_ticked)

    def __on_entity_ticked(self) -> int:
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._animation is None:
            return

        scale_x, scale_y, texture = self._animation.get_frame()

        rect = Graphene.Rect()
        rect.init(0, 0, self.get_width() * scale_x, self.get_height() * scale_y)

        snapshot.append_scaled_texture(texture, Gsk.ScalingFilter.TRILINEAR, rect)

    def update(self, description: Description) -> None:
        self._animation = EntityRegistry.create_animation_from_description(description)


class Entity(Gtk.AspectFrame):
    def __init__(self) -> None:
        super().__init__()

        self._renderer = EntityRenderer()

        self.set_obey_child(False)
        self.set_ratio(1)
        self.set_child(self._renderer)

    def update(self, description: Description) -> None:
        return self._renderer.update(description)
