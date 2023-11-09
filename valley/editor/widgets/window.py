import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Gio, Adw

from .entity_settings import EntitySettings

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "window.ui"))
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    game = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._entity_settings = EntitySettings()
        self.game.props.child = self._entity_settings

    def open(self, path: str) -> None:
        description = Description.new_from_json(path)
        self._entity_settings.description = description.game.default

    def save(self, path: str) -> None:
        description = Description(
            game=Description(
                default=self._entity_settings.description,
            ),
        )

        file = Gio.File.new_for_path(path)
        file.replace_contents(
            contents=description.to_json().encode("UTF-8"),
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.REPLACE_DESTINATION,
            cancellable=None,
        )
