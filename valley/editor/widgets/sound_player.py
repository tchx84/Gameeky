import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import Optional

from gi.repository import Gtk, GLib

from ...common.scanner import Description
from ...common.definitions import TICK

from ...client.sound.entity import SoundSequence


@Gtk.Template(filename=os.path.join(__dir__, "sound_player.ui"))
class SoundPlayer(Gtk.Box):
    __gtype_name__ = "SoundPlayer"

    play_button = Gtk.Template.Child()
    stop_button = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._playing = False
        self._sequence: Optional[SoundSequence] = None
        self._handler_id = GLib.timeout_add(TICK, self.__on_ticked)

    def _play(self) -> None:
        if self._sequence is None:
            return

        self._sequence.play()
        self.play_button.props.visible = False
        self.stop_button.props.visible = True

    def _stop(self) -> None:
        if self._sequence is None:
            return

        self._sequence.stop()
        self.play_button.props.visible = True
        self.stop_button.props.visible = False

    def __on_ticked(self) -> int:
        if self._playing is True:
            self._play()
        else:
            self._stop()

        return GLib.SOURCE_CONTINUE

    @Gtk.Template.Callback("on_play_button_clicked")
    def __on_play_button_clicked(self, button: Gtk.Button) -> None:
        self._playing = True

    @Gtk.Template.Callback("on_stop_button_clicked")
    def __on_stop_button_clicked(self, button: Gtk.Button) -> None:
        self._playing = False

    def update(self, description: Description) -> None:
        if self._sequence is not None:
            self._sequence.stop()

        self._sequence = SoundSequence.new_from_description(description)

    def shutdown(self) -> None:
        if self._handler_id is not None:
            GLib.Source.remove(self._handler_id)

        self._stop()
