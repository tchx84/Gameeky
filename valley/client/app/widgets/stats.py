from gi.repository import Gdk, Gtk

from .status import Status
from .entity import Entity

from ...game.stats import Stats as StatsModel


class Stats(Gtk.Box):
    def __init__(self, model: StatsModel) -> None:
        super().__init__()

        color = Gdk.RGBA()
        color.parse("#0072D6")

        self._durability = Status()
        self._stamina = Status(color)
        self._held = Entity()

        self.append(self._durability)
        self.append(self._stamina)
        self.append(self._held)

        self.props.orientation = Gtk.Orientation.VERTICAL

        self._model = model
        self._model.connect("updated", self.__on_model_updated)

    def __on_model_updated(self, model: StatsModel) -> None:
        self._durability.value = model.durability
        self._stamina.value = model.stamina
        self._held.type_id = model.held
