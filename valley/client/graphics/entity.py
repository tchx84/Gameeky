from typing import Dict, List

from gi.repository import Gdk, GdkPixbuf

from ...common.action import Action
from ...common.direction import Direction
from ...common.entity import Entity as CommonEntity
from ...common.scanner import Description
from ...common.utils import get_time_milliseconds
from ...common.utils import get_data_path


class Animation:
    def __init__(self, duration: float, frames: List[Gdk.Texture]) -> None:
        self._frames = frames
        self._duration = duration * 1000

        self._frame_duration = self._duration / len(self._frames)
        self._start_timestamp = get_time_milliseconds()

    def get_frame(self) -> Gdk.Texture:
        timestamp = get_time_milliseconds()
        elapsed = timestamp - self._start_timestamp

        # Reset animation after long pauses
        if elapsed > self._duration:
            self._start_timestamp = timestamp
            elapsed = 0

        index = int(elapsed / self._frame_duration) % len(self._frames)
        return self._frames[index]


class Entity:
    def __init__(
        self,
        type_id: int,
        scale_x: float,
        scale_y: float,
        default: Animation,
    ) -> None:
        self.type_id = type_id
        self.scale_x = scale_x
        self.scale_y = scale_y
        self._default = default
        self._animations: Dict[Action, Dict[Direction, Animation]] = {}

    def get_texture(self, entity: CommonEntity) -> Gdk.Texture:
        if entity.action not in self._animations:
            return self._default.get_frame()
        if entity.direction not in self._animations[entity.action]:
            return self._default.get_frame()

        return self._animations[entity.action][entity.direction].get_frame()

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
    def get_entity(cls, entity: CommonEntity) -> Entity:
        return cls.__entities__[entity.type_id]

    @classmethod
    def register(cls, description: Description) -> None:
        default = cls.create_animation_from_description(description.graphics.default)

        entity = Entity(
            type_id=description.id,
            scale_x=description.graphics.scale_x,
            scale_y=description.graphics.scale_y,
            default=default,
        )

        for action in description.graphics.actions:
            for direction in action.directions:
                animation = cls.create_animation_from_description(direction.animation)
                entity.add_animation(
                    Action[action.name.upper()],
                    Direction[direction.name.upper()],
                    animation,
                )

        cls.__entities__[entity.type_id] = entity

    @classmethod
    def create_animation_from_description(
        cls,
        description: Description,
    ) -> Animation:
        frames = []

        pixbufs = cls.load_pixbufs_from_image(
            columns=description.columns,
            rows=description.rows,
            path=get_data_path(description.path),
        )

        for pixbuf in pixbufs[description.first_frame : description.last_frame + 1]:
            pixbuf = cls.transform_pixbuf(
                pixbuf=pixbuf,
                crop_x=description.crop_x,
                crop_y=description.crop_y,
                flip_x=description.flip_x,
                flip_y=description.flip_y,
            )

            frames.append(Gdk.Texture.new_for_pixbuf(pixbuf))

        return Animation(duration=description.duration, frames=frames)

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
        if crop_y > 0:
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
