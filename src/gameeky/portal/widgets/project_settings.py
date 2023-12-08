from gi.repository import Gtk, Adw

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/portal/widgets/project_settings.ui")  # fmt: skip
class ProjectSettings(Adw.PreferencesGroup):
    __gtype_name__ = "ProjectSettings"

    _name = Gtk.Template.Child()
    _description = Gtk.Template.Child()

    @property
    def description(self) -> Description:
        return Description(
            name=self._name.props.text,
            description=self._description.props.text,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self._name.props.text = description.name
        self._description.props.text = description.description
