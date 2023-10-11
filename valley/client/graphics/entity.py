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
    def __init__(self, type_id: int, default: Animation) -> None:
        self.type_id = type_id
        self._default = default
        self._animations: Dict[Action, Dict[Direction, Animation]] = {}

    def get_texture(self, action: Action, direction: Direction) -> Gdk.Texture:
        if action not in self._animations:
            return self._default.get_frame()
        if direction not in self._animations[action]:
            return self._default.get_frame()

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
            entity.action,
            entity.direction,
        )

    @classmethod
    def register(cls, description: Description) -> None:
        pixbufs = cls.load_pixbufs_from_image(
            columns=description.graphics.columns,
            rows=description.graphics.rows,
            path=get_data_path(description.graphics.path),
        )

        default = cls.create_animation_from_description(
            pixbufs,
            description.graphics.default,
        )
        entity = Entity(type_id=description.id, default=default)

        for action in description.graphics.actions:
            for direction in action.directions:
                animation = cls.create_animation_from_description(
                    pixbufs,
                    direction.animation,
                )

                entity.add_animation(
                    Action[action.name.upper()],
                    Direction[direction.name.upper()],
                    animation,
                )

        cls.__entities__[entity.type_id] = entity

    @classmethod
    def create_animation_from_description(
        cls,
        pixbufs: List[GdkPixbuf.Pixbuf],
        description: Description,
    ) -> Animation:
        frames = [
            Gdk.Texture.new_for_pixbuf(
                cls.transform_pixbuf(
                    pixbuf=pixbuf,
                    crop_x=description.crop_x,
                    crop_y=description.crop_y,
                    flip_x=description.flip_x,
                    flip_y=description.flip_y,
                )
            )
            for pixbuf in pixbufs[description.first_frame : description.last_frame + 1]
        ]

        return Animation(description.time_per_frame, frames)

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
