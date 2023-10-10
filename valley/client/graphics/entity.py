from typing import Dict, List

from gi.repository import Gdk, GdkPixbuf

from ...common.action import Action
from ...common.direction import Direction
from ...common.entity import Entity as CommonEntity
from ...common.scanner import Description
from ...common.utils import get_monotonic_time_ms
from ...common.utils import get_data_path


class Animation:
    def __init__(self, time_per_frame: int, frames: List[Gdk.Texture]) -> None:
        self._time_per_frame = time_per_frame
        self._frames = frames

    def get_frame(self) -> Gdk.Texture:
        index = int(
            (get_monotonic_time_ms() / self._time_per_frame) % len(self._frames)
        )
        return self._frames[index]


class Entity:
    def __init__(self, type_id: int) -> None:
        self.type_id = type_id
        self._animations: Dict[Action, Dict[Direction, Animation]] = {}

    def get_texture(self, action: Action, direction: Direction) -> Gdk.Texture:
        return self._animations[action][direction].get_frame()

    def add_animation(
        self,
        action: Action,
        direction: Direction,
        animation: Animation,
    ) -> None:
        if action not in self._animations:
            self._animations[action] = {}

        self._animations[action][direction] = animation


class EntityRegistry:
    __entities__: Dict[int, Entity] = {}

    @classmethod
    def get_texture(cls, entity: CommonEntity) -> Gdk.Texture:
        return cls.__entities__[entity.type_id].get_texture(
            entity.action, Direction(entity.angle)
        )

    @classmethod
    def register(cls, description: Description) -> None:
        pixbufs = cls.load_pixbufs_from_image(
            columns=description.graphics.columns,
            rows=description.graphics.rows,
            path=get_data_path(description.graphics.path),
        )

        entity = Entity(type_id=description.type_id)

        for action, directions in vars(description.graphics.actions).items():
            for direction, info in vars(directions).items():
                frames = [
                    Gdk.Texture.new_for_pixbuf(
                        cls.transform_pixbuf(
                            pixbuf=pixbuf,
                            crop_x=info.crop_x,
                            crop_y=info.crop_y,
                            flip_x=info.flip_x,
                            flip_y=info.flip_y,
                        )
                    )
                    for pixbuf in pixbufs[info.first_frame : info.last_frame + 1]
                ]

                entity.add_animation(
                    Action[action.upper()],
                    Direction[direction.upper()],
                    Animation(info.time_per_frame, frames),
                )

        cls.__entities__[entity.type_id] = entity

    @classmethod
    def transform_pixbuf(
        cls,
        pixbuf: GdkPixbuf.Pixbuf,
        crop_x: int = 0,
        crop_y: int = 0,
        flip_x: bool = False,
        flip_y: bool = False,
    ) -> GdkPixbuf.Pixbuf:
        if flip_x is True:
            pixbuf = pixbuf.flip(horizontal=True)
        if flip_y is True:
            pixbuf = pixbuf.flip(horizontal=False)
        if crop_x > 0:
            pixbuf = pixbuf.new_subpixbuf(
                crop_x,
                0,
                pixbuf.get_width() - crop_x,
                pixbuf.get_height(),
            )
        if crop_x > 0:
            pixbuf = pixbuf.new_subpixbuf(
                0,
                crop_y,
                pixbuf.get_width(),
                pixbuf.get_height() - crop_y,
            )

        return pixbuf

    @classmethod
    def load_pixbufs_from_image(
        cls,
        columns: int,
        rows: int,
        path: str,
    ) -> List[GdkPixbuf.Pixbuf]:
        pixbufs = []

        src_pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
        width = int(src_pixbuf.get_width() / columns)
        height = int(src_pixbuf.get_height() / rows)

        for row in range(rows):
            for column in range(columns):
                pixbuf = src_pixbuf.new_subpixbuf(
                    column * width,
                    row * height,
                    width,
                    height,
                )
                pixbufs.append(pixbuf)

        return pixbufs
