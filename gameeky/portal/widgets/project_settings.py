import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "project_settings.ui"))
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
