from typing import Optional

from gi.repository import Gtk, GLib

from .entity import Entity

from ...common.scanner import Description
from ...common.definitions import TICK

from ...client.graphics.entity import Animation as AnimationGraphics, EntityRegistry


class AnimationRenderer(Entity):
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

        scale_x, scale_y, texture = self._animation.get_frame()
        self.do_snapshot_entity(snapshot, scale_x, scale_y, texture)

    def update(self, description: Description) -> None:
        self._animation = EntityRegistry.create_animation_from_description(description)

    def shutdown(self) -> None:
        GLib.Source.remove(self._handler_id)


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

    def shutdown(self) -> None:
        self._renderer.shutdown()
