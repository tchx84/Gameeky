import os

from gi.repository import Gtk, Adw, GObject

from ...common.utils import launch, get_projects_path
from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/portal/widgets/project_row.ui")
class ProjectRow(Adw.ActionRow):
    __gtype_name__ = "ProjectRow"

    __gsignals__ = {
        "edited": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def _launch(self, command) -> None:
        data_path = os.path.join(get_projects_path(), self.props.title)
        launch(command, f"--data_path={data_path}")

    @Gtk.Template.Callback("on_play_clicked")
    def __on_play_clicked(self, button: Gtk.Button) -> None:
        self._launch("dev.tchx84.gameeky.Player")

    @Gtk.Template.Callback("on_scene_clicked")
    def __on_scene_clicked(self, button: Gtk.Button) -> None:
        self._launch("dev.tchx84.gameeky.Scene")

    @Gtk.Template.Callback("on_entity_clicked")
    def __on_entity_clicked(self, button: Gtk.Button) -> None:
        self._launch("dev.tchx84.gameeky.Entity")

    @Gtk.Template.Callback("on_edit_clicked")
    def __on_edit_clicked(self, button: Gtk.Button) -> None:
        self.emit("edited")

    @Gtk.Template.Callback("on_remove_clicked")
    def __on_remove_clicked(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @property
    def description(self) -> Description:
        return Description(
            name=self.props.title,
            description=self.props.subtitle,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.props.title = description.name
        self.props.subtitle = description.description
