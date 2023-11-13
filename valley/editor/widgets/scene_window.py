import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from .entity_row import EntityRow

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "scene_window.ui"))
class SceneWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SceneWindow"

    entities = Gtk.Template.Child()

    def register(self, description: Description) -> None:
        entity = EntityRow()
        entity.description = description
        self.entities.append(entity)
