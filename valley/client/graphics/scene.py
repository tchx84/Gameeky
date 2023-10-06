from typing import Optional

from gi.repository import Gtk

from ..game.scene import Scene as SceneModel


class Scene(Gtk.DrawingArea):
    def __init__(self, model: Optional[SceneModel] = None) -> None:
        super().__init__()

        self._model = model

        self.set_draw_func(self._draw_func, None)

    def _draw_func(self, widget, context, screen_width, screen_height, data=None):
        context.set_source_rgba(0, 0, 0)
        context.rectangle(0, 0, screen_width, screen_height)
        context.fill()

        screen_tile_width = screen_width / self._model.width
        screen_tile_height = screen_height / self._model.height

        screen_offset_x = (screen_width / 2) - (screen_tile_width / 2)
        screen_offset_y = (screen_height / 2) - (screen_tile_height / 2)

        for entity in self._model.entities:
            context.set_source_rgba(1, 1, 1)

            screen_x = (entity.position.x - self._model.anchor.x) * screen_tile_width
            screen_y = (entity.position.y - self._model.anchor.y) * screen_tile_height

            x = screen_x + screen_offset_x
            y = screen_y + screen_offset_y

            context.rectangle(x, y, screen_tile_width, screen_tile_height)

        context.fill()
