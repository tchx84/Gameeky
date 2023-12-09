from gi.repository import Gtk, GObject, Adw

from .project_row import ProjectRow
from .project_new_window import ProjectNewWindow
from .project_edit_window import ProjectEditWindow

from ..models.project import Project

from ...common.monitor import Monitor
from ...common.scanner import Description
from ...common.utils import find_widget_by_id


@Gtk.Template(resource_path="/dev/tchx84/gameeky/portal/widgets/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    __gsignals__ = {
        "reload": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    banner = Gtk.Template.Child()
    content = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._listbox = find_widget_by_id(self.content, "listbox")
        Monitor.default().connect("changed", self.__on_monitor_changed)

    def _add(self, description: Description) -> None:
        row = ProjectRow()
        row.connect("edited", self.__on_edit)
        row.connect("removed", self.__on_removed)
        row.description = description

        self.content.add(row)

    def _remove(self, row: ProjectRow) -> None:
        row.disconnect_by_func(self.__on_edit)
        row.disconnect_by_func(self.__on_removed)

        self.content.remove(row)

    def __on_monitor_changed(self, monitor: Monitor) -> None:
        self.banner.props.revealed = True

    def __on_edit(self, row: ProjectRow) -> None:
        dialog = ProjectEditWindow(transient_for=self)
        dialog.connect("done", self.__on_edit_done, row)
        dialog.present()

        dialog.description = row.description

    def __on_edit_done(self, dialog: ProjectEditWindow, row: ProjectRow) -> None:
        Project.rename(row.description, dialog.description)

    def __on_removed(self, row: ProjectRow) -> None:
        Project.remove(row.description)

    def __on_add_done(self, window: ProjectNewWindow) -> None:
        Project.create(window.description)

    @Gtk.Template.Callback("on_reload_clicked")
    def __on_reload_clicked(self, button: Gtk.Button) -> None:
        self.banner.props.revealed = False
        self.emit("reload")

    def add(self) -> None:
        dialog = ProjectNewWindow(transient_for=self)
        dialog.connect("done", self.__on_add_done)
        dialog.present()

    def load(self, description: Description) -> None:
        self._add(description)

    def reset(self) -> None:
        if self._listbox is None:
            return

        for row in list(self._listbox):
            self._remove(row)
