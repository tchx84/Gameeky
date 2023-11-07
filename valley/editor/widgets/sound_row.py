import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk

from .sound_player import SoundPlayer
from .sound_settings import SoundSettings


@Gtk.Template(filename=os.path.join(__dir__, "sound_row.ui"))
class SoundRow(Gtk.Box):
    __gtype_name__ = "SoundRow"

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._settings = SoundSettings()
        self._settings.connect("changed", self.__on_changed)

        self._player = SoundPlayer()

        self.append(self._settings)
        self.append(self._player)

    def __on_changed(self, settings: SoundSettings) -> None:
        self._player.update(settings.description)
