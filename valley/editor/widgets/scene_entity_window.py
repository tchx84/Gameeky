import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from .entity_settings import EntitySettings

from ..models.scene import Scene as SceneModel, Entity


@Gtk.Template(filename=os.path.join(__dir__, "scene_entity_window.ui"))
class SceneEntityWindow(Adw.Window):
    __gtype_name__ = "SceneEntityWindow"

    content = Gtk.Template.Child()

    def __init__(self, entity: Entity, model: SceneModel, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._entity = entity
        self._model = model

        self._entity_settings = EntitySettings()
        self._entity_settings.description = self._entity.description
        self._entity_settings.connect("changed", self.__on_changed)

        self.content.props.child = self._entity_settings

    def __on_changed(self, button: Gtk.Button) -> None:
        self._entity.description = self._entity_settings.description
