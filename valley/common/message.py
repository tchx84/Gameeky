from typing import Tuple

from gi.repository import GLib

from .action import Action
from .serializeable import Serializeable


class Message(Serializeable):
    SIGNATURE = "(iii)"

    def __init__(
        self,
        session_id: int,
        action: Action = Action.NOTHING,
        sequence: int = 0,
    ) -> None:
        self.session_id = session_id
        self.action = action
        self.sequence = sequence

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(
            self.SIGNATURE, (self.session_id, self.action, self.sequence)
        )

    @classmethod
    def from_values(cls, values: Tuple[int, ...]) -> "Message":
        session_id, action, sequence = values
        return cls(session_id, Action(action), sequence)
