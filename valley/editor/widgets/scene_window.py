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
    area = Gtk.Template.Child()
    time = Gtk.Template.Child()
    zoom_in = Gtk.Template.Child()
    zoom_out = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._scene_model = SceneModel()

        self._scene_view = SceneView()
        self._grid_view = GridView()
        self._grid_view.connect("clicked", self.__on_clicked)

        self.overlay.props.child = self._scene_view
        self.overlay.add_overlay(self._grid_view)

        # XXX Move the UI file somehow
        self.time.connect("notify::selected-item", self.__on_time_changed)

    def __on_time_changed(self, *args) -> None:
        self._scene_model.time = float(self.time.props.selected)
        self._scene_model.refresh()

    def __on_clicked(self, grid: GridView, x: int, y: int) -> None:
        area = int(self.area.props.selected_item.props.string)

        if self.eraser.props.active is True:
            self._scene_model.remove(x, y, area)
            return

        selected = self.entities.get_selected_children()
        if not selected:
            return

        child = selected[0].get_child()
        if not child.type_id:
            return

        self._scene_model.add(child.type_id, x, y, None, area)

    def register(self, description: Description) -> None:
        entity = EntityRow()
        entity.description = description
        self.entities.append(entity)

    @Gtk.Template.Callback("on_zoom_in")
    def __on_zoom_in(self, *args) -> None:
        self._scene_view.scale += 1
        self._grid_view.scale += 1

    @Gtk.Template.Callback("on_zoom_out")
    def __on_zoom_out(self, *args) -> None:
        self._scene_view.scale -= 1
        self._grid_view.scale -= 1

    @Gtk.Template.Callback("on_grid_changed")
    def __on_grid_changed(self, button: Gtk.Button) -> None:
        self._grid_view.props.visible = button.props.active

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
