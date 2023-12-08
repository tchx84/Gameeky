from typing import Optional

from gi.repository import Gtk

from .entity import Entity


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/entity_row.ui")
class EntityRow(Gtk.Box):
    __gtype_name__ = "EntityRow"

    entity = Gtk.Template.Child()
    label = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()

        self._entity = Entity()
        self.entity.props.child = self._entity

    @property
    def type_id(self) -> Optional[int]:
        return self._entity.type_id

    @type_id.setter
    def type_id(self, type_id: int) -> None:
        self._entity.type_id = type_id

    @property
    def name(self) -> str:
        return self.label.props.label

    @name.setter
    def name(self, name: str) -> None:
        self.label.props.label = name
