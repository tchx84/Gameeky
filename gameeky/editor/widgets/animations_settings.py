import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import Dict, Optional

from gi.repository import Gtk

from .animation_row import AnimationRow

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "animations_settings.ui"))
class AnimationsSettings(Gtk.Box):
    __gtype_name__ = "AnimationsSettings"

    button = Gtk.Template.Child()
    animations_box = Gtk.Template.Child()

    def _add(
        self,
        state: Optional[str],
        direction: Optional[str],
        description: Optional[Description],
        prepend: bool = False,
    ) -> None:
        row = AnimationRow()
        row.connect("cloned", self.__on_cloned)
        row.connect("removed", self.__on_removed)

        if state is not None:
            row.state = state
        if direction is not None:
            row.direction = direction
        if description is not None:
            row.description = description

        if prepend is True:
            self.animations_box.prepend(row)
        else:
            self.animations_box.append(row)

    def _remove(self, row: AnimationRow) -> None:
        row.shutdown()
        row.disconnect_by_func(self.__on_cloned)
        row.disconnect_by_func(self.__on_removed)

        self.animations_box.remove(row)

    def __on_removed(self, row: AnimationRow) -> None:
        self._remove(row)

    def __on_cloned(self, row: AnimationRow) -> None:
        self._add(row.state, row.direction, row.description, prepend=True)

    @Gtk.Template.Callback("on_clicked")
    def __on_clicked(self, button: Gtk.Button) -> None:
        self._add(state=None, direction=None, description=None, prepend=True)

    @property
    def description(self) -> Description:
        default: Optional[Description] = None
        states: Dict[str, Description] = {}

        for row in list(self.animations_box):
            if row.state == "default":
                default = row.description
                continue

            if row.state not in states:
                states[row.state] = Description(name=row.state, directions=[])

            states[row.state].directions.append(
                Description(
                    name=row.direction,
                    animation=row.description,
                )
            )

        return Description(
            default=default,
            states=list(states.values()),
        )

    @description.setter
    def description(self, description: Description) -> None:
        for row in list(self.animations_box):
            self._remove(row)

        if description.default is not None:
            self._add("default", None, description.default)

        for state in description.states:
            for direction in state.directions:
                self._add(state.name, direction.name, direction.animation)
