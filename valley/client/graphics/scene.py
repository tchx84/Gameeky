from typing import Optional

from gi.repository import Gtk

from ..game.scene import Scene as SceneModel


class Scene(Gtk.DrawingArea):
    TILES_X = 16
    TILES_Y = 16

    def __init__(self, model: Optional[SceneModel] = None) -> None:
        super().__init__()

        self._model = model

        self.set_draw_func(self._draw_func, None)

    def _draw_func(self, widget, context, width, height, data=None):
        context.set_source_rgba(0, 0, 0)
        context.rectangle(0, 0, width, height)
        context.fill()

        anchor = self._model.anchor

        tile_width = width / self.TILES_X
        tile_height = height / self.TILES_Y
        offset_x = (width / 2) - (tile_width / 2)
        offset_y = (height / 2) - (tile_height / 2)

        for entity in self._model.entities:
            context.set_source_rgba(1, 1, 1)

            x = entity.position.x - anchor.position.x + offset_x
            y = entity.position.y - anchor.position.y + offset_y

            context.rectangle(x, y, tile_width, tile_height)

        context.fill()
