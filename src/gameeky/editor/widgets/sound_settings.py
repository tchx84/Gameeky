from typing import Optional

from gi.repository import Adw, GLib, Gtk, GObject

from .paths_row import PathsRow
from .sound_player import SoundPlayer

from ...common.scanner import Description
from ...common.definitions import DEFAULT_TIMEOUT


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/sound_settings.ui")  # fmt: skip
class SoundSettings(Adw.PreferencesGroup):
    __gtype_name__ = "SoundSettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    preview = Gtk.Template.Child()
    delay = Gtk.Template.Child()
    timeout = Gtk.Template.Child()
    paths = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._handler_id: Optional[int] = None

        self._paths = PathsRow()
        self._paths.connect("changed", self.__on_changed)
        self.paths.append(self._paths)

        self._preview = SoundPlayer()
        self.preview.append(self._preview)

    @Gtk.Template.Callback("on_changed")
    def __on_changed(self, *args) -> None:
        if self._handler_id is not None:
            GLib.Source.remove(self._handler_id)

        self._handler_id = GLib.timeout_add_seconds(
            DEFAULT_TIMEOUT / 2,
            self.__on_change_delayed,
        )

    def __on_change_delayed(self) -> int:
        self._preview.update(self.description)

        self.emit("changed")
        self._handler_id = None
        return GLib.SOURCE_REMOVE

    @property
    def description(self) -> Description:
        return Description(
            delay=round(self.delay.props.value, 1),
            timeout=round(self.timeout.props.value, 1),
            paths=self._paths.paths,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.delay.props.value = description.delay
        self.timeout.props.value = description.timeout
        self._paths.paths = description.paths

    def shutdown(self) -> None:
        self._preview.shutdown()
