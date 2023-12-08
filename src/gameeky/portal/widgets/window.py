from gi.repository import Gtk, Adw

from .project_row import ProjectRow
from .project_new_window import ProjectNewWindow
from .project_edit_window import ProjectEditWindow

from ..models.project import Project

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/portal/widgets/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    content = Gtk.Template.Child()

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

    def __on_edit(self, row: ProjectRow) -> None:
        dialog = ProjectEditWindow(transient_for=self)
        dialog.connect("done", self.__on_edit_done, row)
        dialog.present()

        dialog.description = row.description

    def __on_edit_done(self, dialog: ProjectEditWindow, row: ProjectRow) -> None:
        old_description = row.description
        new_description = dialog.description

        Project.rename(old_description, new_description)

        row.description = new_description

    def __on_removed(self, row: ProjectRow) -> None:
        Project.remove(row.description)

        self._remove(row)

    def __on_add_done(self, window: ProjectNewWindow) -> None:
        description = window.description

        Project.create(description)

        self._add(description)

    def add(self) -> None:
        dialog = ProjectNewWindow(transient_for=self)
        dialog.connect("done", self.__on_add_done)
        dialog.present()

    def load(self, description: Description) -> None:
        self._add(description)
