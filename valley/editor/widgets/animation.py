from typing import Optional

from gi.repository import Gsk, Gtk, GLib, Graphene

from ...common.scanner import Description
from ...common.definitions import TICK

from ...client.graphics.entity import Animation as AnimationGraphics, EntityRegistry


class AnimationRenderer(Gtk.Widget):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._animation: Optional[AnimationGraphics] = None
        self._handler_id = GLib.timeout_add(TICK, self.__on_entity_ticked)

    def __on_entity_ticked(self) -> int:
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._animation is None:
            return

        _, _, texture = self._animation.get_frame()

        rect = Graphene.Rect()
        rect.init(0, 0, self.get_width(), self.get_height())

        snapshot.append_scaled_texture(texture, Gsk.ScalingFilter.TRILINEAR, rect)

    def update(self, description: Description) -> None:
        self._animation = EntityRegistry.create_animation_from_description(description)


class Animation(Gtk.AspectFrame):
    def __init__(self) -> None:
        super().__init__()

        self._renderer = AnimationRenderer()

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_obey_child(False)
        self.set_ratio(1)
        self.set_child(self._renderer)

    def update(self, description: Description) -> None:
        return self._renderer.update(description)
