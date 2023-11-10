import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import Optional

from gi.repository import Gtk

from .sound_row import SoundRow

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "sounds_settings.ui"))
class SoundsSettings(Gtk.Box):
    __gtype_name__ = "SoundsSettings"

    sounds_box = Gtk.Template.Child()

    def _add(
        self,
        state: Optional[str],
        description: Optional[Description],
        prepend: bool = False,
    ) -> None:
        row = SoundRow()
        row.connect("removed", self.__on_removed)

        if state is not None:
            row.state = state
        if description is not None:
            row.description = description

        if prepend is True:
            self.sounds_box.prepend(row)
        else:
            self.sounds_box.append(row)

    def _remove(self, row: SoundRow) -> None:
        row.shutdown()
        row.disconnect_by_func(self.__on_removed)

        self.sounds_box.remove(row)

    def __on_removed(self, row: SoundRow) -> None:
        self._remove(row)

    @Gtk.Template.Callback("on_clicked")
    def __on_clicked(self, button: Gtk.Button) -> None:
        self._add(state=None, description=None, prepend=True)

    @property
    def description(self) -> Description:
        return Description(
            states=[
                Description(name=row.state, sequence=row.description)
                for row in list(self.sounds_box)
            ]
        )

    @description.setter
    def description(self, description: Description) -> None:
        for row in list(self.sounds_box):
            self._remove(row)

        for state in description.states:
            self._add(state.name, state.sequence)
