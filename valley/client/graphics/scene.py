from gi.repository import Gtk, Graphene

from .entity import EntityRegistry
from .status import Status
from ..game.scene import Scene as SceneModel


class Scene(Gtk.Widget):
    def __init__(self, model: SceneModel) -> None:
        super().__init__()

        self._model = model
        self._model.connect("ticked", self.__on_scene_updated)
        self._model.connect("updated", self.__on_scene_updated)

    def __on_scene_updated(self, model: SceneModel) -> None:
        self.queue_draw()

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / self._model.width
        tile_height = screen_height / self._model.height

        for entity in self._model.entities:
            if entity.visible is False:
                continue

            scale_x, scale_y, texture = EntityRegistry.get_texture(entity)

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

            Status.draw(
                snapshot,
                entity,
                rect_x,
                rect_y,
                rect_width,
                rect_height,
                tile_width,
                tile_height,
            )
