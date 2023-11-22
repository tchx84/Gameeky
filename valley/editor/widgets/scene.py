from typing import Tuple

from gi.repository import Gtk

from ...common.utils import clamp
from ...client.graphics.scene import Scene as SceneGraphics


class Scene(SceneGraphics):
    TILE_SIZE = 10

    def __init__(self) -> None:
        super().__init__(editing=True)
        self._scale = 1.0

        self.props.hexpand = True
        self.props.vexpand = True

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE

    def do_measure(
        self,
        orientation: Gtk.Orientation,
        for_size: int,
    ) -> Tuple[float, ...]:
        if self._model is None:
            return (0, 0, -1, -1)

        if orientation == Gtk.Orientation.HORIZONTAL:
            width = self._model.width * self.TILE_SIZE * self.scale
            return (width, width, -1, -1)
        else:
            height = self._model.height * self.TILE_SIZE * self.scale
            return (height, height, -1, -1)

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        self._scale = clamp(10.0, 1.0, scale)
        self.queue_resize()
