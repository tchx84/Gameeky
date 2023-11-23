import math

from typing import Optional

from gi.repository import Gtk, Gdk, GLib

from ..game.service import Service

from ...common.logger import logger
from ...common.vector import Vector
from ...common.entity import Entity
from ...common.scene import Scene
from ...common.definitions import Action, Direction, TICK, TILES_X, TILES_Y
from ...common.utils import add_timeout_source, remove_source_id


class Cursor:
    def __init__(self, widget: Gtk.Widget, model: Scene, service: Service) -> None:
        super().__init__()
        self._service = service
        self._model = model

        self._right_click = Gtk.GestureClick()
        self._right_click.set_button(Gdk.BUTTON_PRIMARY)
        self._right_click.connect("pressed", self.__on_right_pressed)

        self._left_click = Gtk.GestureClick()
        self._left_click.set_button(Gdk.BUTTON_SECONDARY)
        self._left_click.connect("pressed", self.__on_left_pressed)

        self._widget = widget

        self._popover = self._widget.popover
        self._performed_source_id = self._popover.connect(
            "performed",
            self.__on_action_perfomed,
        )

        self._canvas = self._widget.canvas
        self._canvas.add_controller(self._right_click)
        self._canvas.add_controller(self._left_click)

        self._target: Optional[Vector] = None
        self._timeout_source_id = add_timeout_source(TICK, self.__on_tick)

    def _find(self, position: Vector) -> Optional[Entity]:
        for entity in self._model.entities:
            if entity.position == position:
                return entity

        return None

    def __on_tick(self, *args) -> int:
        if self._target is None:
            return GLib.SOURCE_CONTINUE

        if (player := self._find(self._model.anchor)) is None:
            return GLib.SOURCE_CONTINUE

        x = (
            math.floor(player.position.x)
            if player.direction == Direction.WEST
            else math.ceil(player.position.x)
        )
        y = (
            math.floor(player.position.y)
            if player.direction == Direction.NORTH
            else math.ceil(player.position.y)
        )

        direction: Optional[Direction] = None

        if self._target.x < x:
            direction = Direction.WEST
        elif self._target.x > x:
            direction = Direction.EAST
        elif self._target.y < y:
            direction = Direction.NORTH
        elif self._target.y > y:
            direction = Direction.SOUTH

        if direction is not None:
            self._service.message(Action.MOVE, direction)
        else:
            self._service.message(Action.IDLE, 0)
            self._target = None

        return GLib.SOURCE_CONTINUE

    def __on_right_pressed(
        self,
        controller: Gtk.GestureClick,
        n_press: int,
        x: float,
        y: float,
    ) -> None:
        center_x = math.floor(TILES_X / 2)
        center_y = math.floor(TILES_Y / 2)

        canvas_x = math.floor(x / (self._canvas.get_width() / TILES_X))
        canvas_y = math.floor(y / (self._canvas.get_height() / TILES_Y))

        delta_x = canvas_x - center_x
        delta_y = canvas_y - center_y

        if delta_x == 0 and delta_y == 0:
            return

        anchor_x = math.floor(self._model.anchor.x)
        anchor_y = math.floor(self._model.anchor.y)

        self._target = Vector(
            x=anchor_x + delta_x,
            y=anchor_y + delta_y,
        )

    def __on_left_pressed(
        self,
        controller: Gtk.GestureClick,
        n_press: int,
        x: float,
        y: float,
    ) -> None:
        self._widget.display_actions(x, y)

    def __on_action_perfomed(self, popover: Gtk.Popover, action: Action) -> None:
        self._service.message(action, 0)
        self._target = None

    def shutdown(self) -> None:
        if self._timeout_source_id is not None:
            remove_source_id(self._timeout_source_id)

        self._popover.disconnect(self._performed_source_id)

        self._canvas.remove_controller(self._right_click)
        self._canvas.remove_controller(self._left_click)

        logger.info("Client.Cursor.shut")
