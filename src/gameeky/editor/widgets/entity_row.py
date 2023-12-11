from typing import Optional

from gi.repository import Gtk

from .entity import Entity

from ..models.entity_row import EntityRow as EntityRowModel


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/entity_row.ui")
class EntityRow(Gtk.Box):
    __gtype_name__ = "EntityRow"

    entity = Gtk.Template.Child()
    label = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()

        self._model = EntityRowModel(type_id=0, name="", path="")
        self._entity = Entity()
        self.entity.props.child = self._entity

    @property
    def type_id(self) -> Optional[int]:
        return self._mdoel.props.type_id

    @property
    def name(self) -> str:
        return self._model.props.name

    @property
    def model(self) -> EntityRowModel:
        return self._model

    @model.setter
    def model(self, model: EntityRowModel) -> None:
        self._model = model

        self._entity.type_id = self._model.props.type_id
        self.label.props.label = self._model.props.name
