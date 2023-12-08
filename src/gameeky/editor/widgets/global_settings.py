from gi.repository import Gtk, Adw

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/global_settings.ui")  # fmt: skip
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
            graphics=None,
            sound=None,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.identifier.props.value = description.id
