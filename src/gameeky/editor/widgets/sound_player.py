# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from gi.repository import Gtk, GLib

from ...common.scanner import Description
from ...common.definitions import TICK

from ...client.sound.entity import SoundSequence


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/sound_player.ui")  # fmt: skip
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
