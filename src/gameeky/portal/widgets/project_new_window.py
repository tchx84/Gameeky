from gi.repository import Gtk, Adw, GObject

from .project_settings import ProjectSettings

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/portal/widgets/project_new_window.ui")  # fmt: skip
class ProjectNewWindow(Adw.Window):
    __gtype_name__ = "ProjectNewWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    content = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._project_settings = ProjectSettings()
        self.content.props.child = self._project_settings

    def _notify(self, title) -> None:
        toast = Adw.Toast()
        toast.props.title = title
        toast.props.timeout = 3

        self.toast.add_toast(toast)

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_create_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        description = self.description

        if not description.name:
            self._notify("A valid name must be provided")
            return

        if not description.description:
            self._notify("A valid description must be provided")
            return

        self.emit("done")
        self.close()

    @property
    def description(self) -> Description:
        return self._project_settings.description
