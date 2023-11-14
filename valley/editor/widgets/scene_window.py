import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from .scene import Scene as SceneView
from .grid import Grid as GridView
from .entity_row import EntityRow

from ..models.scene import Scene as SceneModel

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "scene_window.ui"))
class SceneWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SceneWindow"

    entities = Gtk.Template.Child()
    aspect = Gtk.Template.Child()
    overlay = Gtk.Template.Child()
    eraser = Gtk.Template.Child()
    layer = Gtk.Template.Child()
    area = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._scene_model = SceneModel()

        self._scene_view = SceneView()
        self._grid_view = GridView()
        self._grid_view.connect("clicked", self.__on_clicked)

        self.overlay.props.child = self._scene_view
        self.overlay.add_overlay(self._grid_view)

    def __on_clicked(self, grid: GridView, x: int, y: int) -> None:
        layer = self.layer.props.selected
        area = int(self.area.props.selected_item.props.string)

        if self.eraser.props.active is True:
            self._scene_model.remove(x, y, layer, area)
            return

        selected = self.entities.get_selected_children()
        if not selected:
            return

        child = selected[0].get_child()
        if not child.type_id:
            return

        self._scene_model.add(child.type_id, x, y, layer, area)

    def register(self, description: Description) -> None:
        entity = EntityRow()
        entity.description = description
        self.entities.append(entity)

    @property
    def description(self) -> Description:
        return Description()

    @description.setter
    def description(self, description: Description) -> None:
        self._scene_model.description = description

        self.aspect.props.ratio = self._scene_model.ratio

        self._grid_view.columns = self._scene_model.width
        self._grid_view.rows = self._scene_model.height
        self._grid_view.scale = 1.0

        self._scene_view.model = self._scene_model
        self._scene_view.scale = 1.0
