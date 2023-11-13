import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import Optional

from gi.repository import Gtk

from .entity import Entity

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "entity_row.ui"))
class EntityRow(Gtk.Box):
    __gtype_name__ = "EntityRow"

    entity = Gtk.Template.Child()
    label = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._description: Optional[Description] = None

        self._entity = Entity()
        self.entity.props.child = self._entity

    @property
    def description(self) -> Optional[Description]:
        return self._description

    @description.setter
    def description(self, description: Description) -> None:
        self._entity.type_id = description.id
        self._entity.visible = description.game.default.visible
        self.label.props.label = description.game.default.name
        self._description = description
