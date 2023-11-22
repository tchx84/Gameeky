from typing import Optional
from gi.repository import Gtk, GLib, Gdk, Gsk, Graphene

from .entity import EntityRegistry
from .status import Status
from ..game.scene import Scene as SceneModel
from ..definitions import Alpha, Normalized

from ...common.utils import oscillate
from ...common.definitions import TICK


class Scene(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._model: Optional[SceneModel] = None
        self._layer: Optional[int] = None
        self.editing = False

        GLib.timeout_add(TICK, self.__on_tick)

    def __on_tick(self) -> int:
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def _do_snapshot_time(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / self._model.width
        tile_height = screen_height / self._model.height

        alpha = oscillate(Alpha.MAX, Alpha.MIN, self._model.time)

        black = Gdk.RGBA()
        black.parse(f"rgba(0,0,0,{alpha})")

        yellow = Gdk.RGBA()
        yellow.parse(f"rgba(255,200,200,{alpha})")

        darkness = Graphene.Rect().init(-1, -1, screen_width + 2, screen_height + 2)
        snapshot.append_color(black, darkness)

        snapshot.push_blur(tile_width * 1.5)

        for entity in self._model.entities:
            if entity.luminance == 0:
                continue

            rect_width = tile_width * 4 * entity.luminance
            rect_height = tile_height * 4 * entity.luminance

            screen_x = (entity.position.x - self._model.anchor.x) * tile_width
            screen_y = (entity.position.y - self._model.anchor.y) * tile_height

            offset_x = (screen_width / 2) - (rect_width / 2)
            offset_y = (screen_height / 2) - (rect_height / 2)

            rect_x = screen_x + offset_x
            rect_y = screen_y + offset_y

            light = Graphene.Rect().init(rect_x, rect_y, rect_width, rect_height)
            snapshot.append_color(yellow, light)

        snapshot.pop()

    def _do_snapshot_entities(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / self._model.width
        tile_height = screen_height / self._model.height

        clip = Graphene.Rect()
        clip.init(0, 0, screen_width, screen_height)

        snapshot.push_clip(clip)

        for entity in self._model.entities:
            if self.editing is False and entity.visible is False:
                continue
            if self.layer is not None and entity.position.z != self.layer:
                continue

            scale_x, scale_y, texture = EntityRegistry.get_texture(entity)

            if texture is None:
                continue

            screen_x = (entity.position.x - self._model.anchor.x) * tile_width
            screen_y = (entity.position.y - self._model.anchor.y) * tile_height

            rect_width = tile_width * scale_x
            rect_height = tile_height * scale_y

            offset_x = (screen_width / 2) - (rect_width / 2)
            offset_y = (screen_height / 2) + (tile_height / 2) - rect_height

            rect_x = screen_x + offset_x
            rect_y = screen_y + offset_y

            entity_rect = Graphene.Rect()
            entity_rect.init(rect_x, rect_y, rect_width, rect_height)

            snapshot.append_texture(texture, entity_rect)

            if entity.status == Normalized.MAX:
                continue

            Status.draw(
                snapshot,
                entity.status,
                rect_x + (rect_width / 2) - (tile_width / 2),
                rect_y,
                tile_width,
                tile_height * 0.2,
            )

        snapshot.pop()

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        snapshot.push_blend(Gsk.BlendMode.MULTIPLY)

        self._do_snapshot_time(snapshot)
        snapshot.pop()

        self._do_snapshot_entities(snapshot)
        snapshot.pop()

    @property
    def layer(self) -> Optional[int]:
        return self._layer

    @layer.setter
    def layer(self, layer: Optional[int]) -> None:
        self._layer = layer
        self.queue_draw()

    @property
    def model(self) -> Optional[SceneModel]:
        return self._model

    @model.setter
    def model(self, model: Optional[SceneModel]) -> None:
        self._model = model
        self.queue_draw()
