from typing import Optional

from gi.repository import Gtk

from ..game.scene import Scene as SceneModel


class Scene(Gtk.DrawingArea):
    TILES_X: int = 17
    TILES_Y: int = 13
    TILES_SIZE: int = 32

    WIDTH: int = TILES_X * TILES_SIZE
    HEIGHT: int = TILES_Y * TILES_SIZE

    def __init__(self, model: Optional[SceneModel] = None) -> None:
        super().__init__()

        self._model = model

        self.set_content_width(self.WIDTH)
        self.set_content_height(self.HEIGHT)
        self.set_draw_func(self._draw_func, None)

    def _draw_func(self, widget, context, width, height, data=None):
        context.set_source_rgba(0, 0, 0)
        context.rectangle(0, 0, self.WIDTH, self.HEIGHT)
        context.fill()

        anchor = self._model.anchor
        half_tile = self.TILES_SIZE / 2
        half_width = self.WIDTH / 2
        half_height = self.HEIGHT / 2

        for entity in self._model.entities:
            context.set_source_rgba(1, 1, 1)

            x = (entity.position.x - anchor.position.x) + half_width - half_tile
            y = (entity.position.y - anchor.position.y) + half_height - half_tile

            context.rectangle(x, y, self.TILES_SIZE, self.TILES_SIZE)

        context.fill()
