from typing import Dict, List

from gi.repository import Gdk, GdkPixbuf

from ...common.action import Action
from ...common.direction import Direction
from ...common.entity import Entity as CommonEntity
from ...common.scanner import Description
from ...common.utils import get_monotonic_time_ms
from ...common.utils import get_data_path


class Entity:
    def __init__(self, type_id: int, ms_per_frame: int) -> None:
        self.type_id = type_id
        self._ms_per_frame = ms_per_frame
        self._frames: Dict[Action, Dict[Direction, List[Gdk.Texture]]] = {}

    def _get_texture(self, action: Action, direction: Direction) -> Gdk.Texture:
        index = int(
            (get_monotonic_time_ms() / self._ms_per_frame)
            % len(self._frames[action][direction])
        )
        return self._frames[action][direction][index]

    def add_frames(
        self, action: Action, direction: Direction, frames: List[Gdk.Texture]
    ) -> None:
        if action not in self._frames:
            self._frames[action] = {}

        self._frames[action][direction] = frames


class EntityRegistry:
    __entities__: Dict[int, Entity] = {}

    @classmethod
    def get_texture(cls, entity: CommonEntity) -> Gdk.Texture:
        return cls.__entities__[entity.type_id]._get_texture(
            entity.action, Direction(entity.angle)
        )

    @classmethod
    def register(cls, description: Description) -> None:
        pixbufs = cls.load_pixbufs_from_image(
            frames_x=description.graphics.frames_x,
            frames_y=description.graphics.frames_y,
            path=get_data_path(description.graphics.path),
        )

        entity = Entity(
            type_id=description.type_id,
            ms_per_frame=description.graphics.ms_per_frame,
        )

        for action, directions in vars(description.graphics.actions).items():
            for direction, info in vars(directions).items():
                frames = [
                    cls.load_texture_from_pixbuf(
                        pixbuf=pixbuf,
                        offset_x=info.offset_x,
                        offset_y=info.offset_y,
                        flip_x=info.flip_x,
                        flip_y=info.flip_y,
                    )
                    for pixbuf in pixbufs[info.first_frame : info.last_frame + 1]
                ]

                entity.add_frames(
                    Action[action.upper()],
                    Direction[direction.upper()],
                    frames,
                )

        cls.__entities__[entity.type_id] = entity

    @classmethod
    def load_texture_from_pixbuf(
        cls,
        pixbuf: GdkPixbuf.Pixbuf,
        offset_x: int = 0,
        offset_y: int = 0,
        flip_x: bool = False,
        flip_y: bool = False,
    ) -> Gdk.Texture:
        if flip_x is True:
            pixbuf = pixbuf.flip(horizontal=True)
        if flip_y is True:
            pixbuf = pixbuf.flip(horizontal=False)
        if offset_x > 0:
            pixbuf = pixbuf.new_subpixbuf(
                offset_x,
                0,
                pixbuf.get_width() - offset_x,
                pixbuf.get_height(),
            )
        if offset_x > 0:
            pixbuf = pixbuf.new_subpixbuf(
                0,
                offset_y,
                pixbuf.get_width(),
                pixbuf.get_height() - offset_y,
            )

        return Gdk.Texture.new_for_pixbuf(pixbuf)

    @classmethod
    def load_pixbufs_from_image(
        cls,
        frames_x: int,
        frames_y: int,
        path: str,
    ) -> List[GdkPixbuf.Pixbuf]:
        pixbufs = []

        src_pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
        frame_width = int(src_pixbuf.get_width() / frames_x)
        frame_height = int(src_pixbuf.get_height() / frames_y)

        for frame_y in range(frames_y):
            for frame_x in range(frames_x):
                pixbuf = src_pixbuf.new_subpixbuf(
                    frame_x * frame_width,
                    frame_y * frame_height,
                    frame_width,
                    frame_height,
                )
                pixbufs.append(pixbuf)

        return pixbufs
