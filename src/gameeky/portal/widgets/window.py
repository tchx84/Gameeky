from gi.repository import Gtk, Gio, GObject, Adw

from .project_row import ProjectRow
from .project_new_window import ProjectNewWindow
from .project_edit_window import ProjectEditWindow

from ..models.project import Project

from ...common.monitor import Monitor
from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/portal/widgets/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    __gsignals__ = {
        "reload": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    banner = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    content = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._ignore = False
        Monitor.default().connect("changed", self.__on_monitor_changed)

    def _add(self, description: Description) -> None:
        row = ProjectRow()
        row.connect("edited", self.__on_edit)
        row.connect("removed", self.__on_removed)
        row.description = description

        self.content.append(row)
        self.stack.set_visible_child_name("projects")

    def _remove(self, row: ProjectRow) -> None:
        row.disconnect_by_func(self.__on_edit)
        row.disconnect_by_func(self.__on_removed)

        self.content.remove(row)

    def __on_monitor_changed(self, monitor: Monitor) -> None:
        self.banner.props.revealed = not self._ignore
        self._ignore = False

    def __on_edit(self, row: ProjectRow) -> None:
        dialog = ProjectEditWindow(transient_for=self)
        dialog.connect("done", self.__on_edit_done, row)
        dialog.present()

        dialog.description = row.description

    def __on_edit_done(self, dialog: ProjectEditWindow, row: ProjectRow) -> None:
        self._ignore = True

        old_description = row.description
        new_description = dialog.description
        Project.rename(old_description, new_description)

        row.description = new_description

    def __on_removed(self, row: ProjectRow) -> None:
        dialog = Gtk.AlertDialog()
        dialog.props.message = "Remove"
        dialog.props.detail = "Are you sure you want to remove this project?"
        dialog.props.buttons = ["Cancel", "Remove"]
        dialog.props.cancel_button = 0
        dialog.props.default_button = 1
        dialog.choose(self, None, self.__on_removed_chosen, row)

    def __on_removed_chosen(
        self,
        dialog: Gtk.AlertDialog,
        result: Gio.AsyncResult,
        row: ProjectRow,
    ) -> None:
        if not dialog.choose_finish(result):
            return

        self._ignore = True

        Project.remove(row.description)

        self._remove(row)

    def __on_add_done(self, window: ProjectNewWindow) -> None:
        self._ignore = True

        description = window.description
        Project.create(description)

        self._add(description)

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
        self.content.remove_all()
        self._ignore = False
        self.stack.set_visible_child_name("landing")
