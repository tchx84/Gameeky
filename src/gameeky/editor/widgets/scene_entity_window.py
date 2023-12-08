from gi.repository import Gtk, Adw

from .entity_settings import EntitySettings

from ..models.scene import Scene as SceneModel, Entity


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/scene_entity_window.ui")  # fmt: skip
class SceneEntityWindow(Adw.Window):
    __gtype_name__ = "SceneEntityWindow"

    content = Gtk.Template.Child()

    def __init__(self, entity: Entity, model: SceneModel, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._entity = entity
        self._model = model

        self._entity_settings = EntitySettings()
        self._entity_settings.description = self._entity.description

        self.content.props.child = self._entity_settings

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_save_clicked")
    def __on_save_clicked(self, button: Gtk.Button) -> None:
        self._entity.description = self._entity_settings.description
        self.destroy()
