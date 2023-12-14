import os

from gi.repository import Gtk, GObject

from ...common.utils import launch, get_projects_path, valid_file
from ...common.monitor import Monitor
from ...common.scanner import Description
from ...common.definitions import DEFAULT_SCENE


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/project_row.ui")
class ProjectRow(Gtk.FlowBoxChild):
    __gtype_name__ = "ProjectRow"

    __gsignals__ = {
        "edited": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    title = Gtk.Template.Child()
    subtitle = Gtk.Template.Child()
    play = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._monitor = Monitor()

    def _get_project_path(self, *path) -> str:
        return os.path.join(get_projects_path(), self.title.props.label, *path)

    def _launch(self, command: str, filename: str) -> None:
        launch(command, f"--project_path={self._get_project_path()} {filename}")

    def _update_button(self) -> None:
        self.play.props.sensitive = valid_file(self._get_project_path(DEFAULT_SCENE))

    def __on_monitor_changed(self, monitor: Monitor) -> None:
        self._update_button()

    @Gtk.Template.Callback("on_play_clicked")
    def __on_play_clicked(self, button: Gtk.Button) -> None:
        self._launch("dev.tchx84.Gameeky.Player", DEFAULT_SCENE)

    @Gtk.Template.Callback("on_edit_clicked")
    def __on_edit_clicked(self, button: Gtk.Button) -> None:
        self._launch("dev.tchx84.Gameeky.Scene", DEFAULT_SCENE)

    @Gtk.Template.Callback("on_settings_clicked")
    def __on_settings_clicked(self, button: Gtk.Button) -> None:
        self.emit("edited")

    @Gtk.Template.Callback("on_remove_clicked")
    def __on_remove_clicked(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @property
    def description(self) -> Description:
        return Description(
            name=self.title.props.label,
            description=self.subtitle.props.label,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.title.props.label = description.name
        self.subtitle.props.label = description.description

        self._monitor.shutdown()
        self._monitor.add(self._get_project_path("scenes"))
        self._monitor.connect("changed", self.__on_monitor_changed)

        self._update_button()

    def shutdown(self) -> None:
        self._monitor.disconnect_by_func(self.__on_monitor_changed)
        self._monitor.shutdown()
