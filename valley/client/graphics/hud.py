from typing import Optional
from gi.repository import Gtk, Graphene

from .status import Status
from .entity import EntityRegistry

from ..game.stats import Stats as StatsModel

from ...common import colors
from ...common.definitions import EntityType, TILES_X, TILES_Y


class Hud(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._model: Optional[StatsModel] = None

    def __on_model_updated(self, model: StatsModel) -> None:
        self.queue_draw()

    def _do_snapshot_entity(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / TILES_X
        tile_height = screen_height / TILES_Y

        rect = Graphene.Rect()
        rect.init(0, 0, tile_width / 2, tile_height / 2)

        snapshot.append_color(colors.BLACK, rect)

        rect = Graphene.Rect()
        rect.init(0, 0, tile_width / 2, tile_height / 2)

        snapshot.append_color(colors.BLACK, rect)

        if self._model.held == EntityType.EMPTY:
            return

        _, _, texture = EntityRegistry.get_default_texture(self._model.held)

        snapshot.append_texture(texture, rect)

    def _do_snapshot_status(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / TILES_X
        tile_height = screen_height / TILES_Y

        Status.draw(
            snapshot,
            self._model.durability,
            tile_width / 2,
            0,
            tile_width * 3,
            tile_height / 4,
        )

        Status.draw(
            snapshot,
            self._model.stamina,
            tile_width / 2,
            tile_height / 4,
            tile_width * 3,
            tile_height / 4,
            colors.BLUE,
        )

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._model is None:
            return

        screen_width = self.get_width()
        screen_height = self.get_height()

        tile_width = screen_width / TILES_X
        tile_height = screen_height / TILES_Y

        anchor = Graphene.Point()
        anchor.init(
            x=(screen_width / 2) - (tile_width * 1.75),
            y=screen_height - tile_height,
        )

        snapshot.translate(anchor)

        self._do_snapshot_entity(snapshot)
        self._do_snapshot_status(snapshot)

    @property
    def model(self) -> Optional[StatsModel]:
        return self._model

    @model.setter
    def model(self, model: Optional[StatsModel]) -> None:
        if self._model is not None:
            self._model.disconnect_by_func(self.__on_model_updated)

        self._model = model

        if self._model is not None:
            self._model.connect("updated", self.__on_model_updated)
