import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "global_settings.ui"))
class GlobalSettings(Adw.PreferencesGroup):
    __gtype_name__ = "GlobalSettings"

    identifier = Gtk.Template.Child()

    @property
    def description(self) -> Description:
        return Description(
            id=int(self.identifier.props.value),
            game=Description(
                default=None,
            ),
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.identifier.props.value = description.id
