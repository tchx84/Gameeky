from gi.repository import Gtk, Graphene

from ...graphics.entity import EntityRegistry

from ....common.definitions import EntityType


class EntityRenderer(Gtk.Widget):
    def __init__(self) -> None:
        super().__init__()
        self._type_id: int = EntityType.EMPTY

        self.props.vexpand = True
        self.props.hexpand = True

    def do_snapshot(self, snapshot: Gtk.Snapshot) -> None:
        if self._type_id == EntityType.EMPTY:
            return

        width = self.get_width()
        height = self.get_height()

        rect = Graphene.Rect()
        rect.init(0, 0, width, height)

        _, _, texture = EntityRegistry.get_default_texture(self._type_id)

        snapshot.append_texture(texture, rect)

    @property
    def type_id(self) -> float:
        return self._type_id

    @type_id.setter
    def type_id(self, type_id) -> None:
        self._type_id = type_id
        self.queue_draw()


class Entity(Gtk.AspectFrame):
    def __init__(self) -> None:
        super().__init__()

        self._renderer = EntityRenderer()

        self.set_obey_child(False)
        self.set_ratio(1)
        self.set_child(self._renderer)

    @property
    def type_id(self) -> float:
        return self._renderer.type_id

    @type_id.setter
    def type_id(self, type_id) -> None:
        self._renderer.type_id = type_id
