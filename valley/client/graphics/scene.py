import math

from gi.repository import Gtk, Graphene

from .entity import EntityRegistry
from ..game.scene import Scene as SceneModel


class Scene(Gtk.Widget):
    def __init__(self, model: SceneModel) -> None:
        super().__init__()

        self._model = model
        self._model.connect("updated", self.__on_scene_updated)

    def __on_scene_updated(self, model: SceneModel) -> None:
        self.queue_draw()

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        screen_width = self.get_width()
        screen_height = self.get_height()

        screen_tile_width = math.ceil(screen_width / self._model.width)
        screen_tile_height = math.ceil(screen_height / self._model.height)

        screen_offset_x = math.ceil((screen_width / 2) - (screen_tile_width / 2))
        screen_offset_y = math.ceil((screen_height / 2) - (screen_tile_height / 2))

        for entity in self._model.entities:
            screen_x = (entity.position.x - self._model.anchor.x) * screen_tile_width
            screen_y = (entity.position.y - self._model.anchor.y) * screen_tile_height

            x = screen_x + screen_offset_x
            y = screen_y + screen_offset_y

            if x + screen_tile_width < 0 or x > screen_width:
                continue
            if y + screen_tile_height < 0 or y > screen_height:
                continue

            entity_rect = Graphene.Rect()
            entity_rect.init(x, y, screen_tile_width, screen_tile_width)

            snapshot.append_texture(EntityRegistry.get_texture(entity), entity_rect)
