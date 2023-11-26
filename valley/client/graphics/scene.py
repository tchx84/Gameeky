import os
import math

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import Optional
from gi.repository import Gtk, GLib, Gdk, Gsk, Graphene

from .entity import EntityRegistry
from .status import Status
from ..game.scene import Scene as SceneModel
from ..definitions import Alpha, Normalized

from ...common import colors
from ...common.utils import oscillate
from ...common.definitions import TICK, GRAPHICS_FILTER


class Scene(Gtk.Widget):
    def __init__(self, editing: Optional[bool] = False) -> None:
        super().__init__()
        self._model: Optional[SceneModel] = None
        self._layer: Optional[int] = None
        self._editing = editing

        self._scaling = Gsk.ScalingFilter(GRAPHICS_FILTER)
        self._lightmap = Gdk.Texture.new_from_filename(
            os.path.join(__dir__, "lightmap.png")
        )

        self._updated_source_id: Optional[int] = None
        self._timeout_source_id: Optional[int] = None

    def __on_updated(self, *args) -> int:
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def _do_snapshot_time(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = math.floor(screen_width / self._model.width)
        tile_height = math.floor(screen_height / self._model.height)

        alpha = oscillate(Alpha.MAX, Alpha.MIN, self._model.time)

        snapshot.push_opacity(alpha)

        darkness = Graphene.Rect().init(-1, -1, screen_width + 2, screen_height + 2)
        snapshot.append_color(colors.BLACK, darkness)

        for entity in self._model.entities:
            if entity.luminance == 0:
                continue

            rect_width = tile_width * 8 * entity.luminance
            rect_height = tile_height * 8 * entity.luminance

            screen_x = (entity.position.x - self._model.anchor.x) * tile_width
            screen_y = (entity.position.y - self._model.anchor.y) * tile_height

            offset_x = (screen_width / 2) - (rect_width / 2)
            offset_y = (screen_height / 2) - (rect_height / 2)

            rect_x = screen_x + offset_x
            rect_y = screen_y + offset_y

            light = Graphene.Rect().init(rect_x, rect_y, rect_width, rect_height)
            snapshot.append_texture(self._lightmap, light)

        snapshot.pop()

    def _do_snapshot_entities(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = math.floor(screen_width / self._model.width)
        tile_height = math.floor(screen_height / self._model.height)

        for entity in self._model.entities:
            if self._editing is False and entity.visible is False:
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

            offset_x = (screen_width / 2) - ((rect_width - tile_width) / 2)
            offset_y = (screen_height / 2) - (rect_height - tile_height)

            rect_x = screen_x + offset_x
            rect_y = screen_y + offset_y

            entity_rect = Graphene.Rect()
            entity_rect.init(rect_x, rect_y, rect_width, rect_height)

            snapshot.append_scaled_texture(texture, self._scaling, entity_rect)

            if entity.status == Normalized.MIN:
                continue
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

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        clip = Graphene.Rect()
        clip.init(0, 0, screen_width, screen_height)

        snapshot.push_clip(clip)

        snapshot.push_blend(Gsk.BlendMode.MULTIPLY)

        self._do_snapshot_time(snapshot)
        snapshot.pop()

        self._do_snapshot_entities(snapshot)
        snapshot.pop()

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
        if self._timeout_source_id is not None:
            GLib.Source.remove(self._timeout_source_id)

        if self._updated_source_id is not None and self._model is not None:
            self._model.disconnect(self._updated_source_id)

        self._timeout_source_id = None
        self._updated_source_id = None

        if self._editing is False and model is not None:
            self._timeout_source_id = GLib.timeout_add(TICK, self.__on_updated)

        if self._editing is True and model is not None:
            self._updated_source_id = model.connect("updated", self.__on_updated)

        self._model = model
